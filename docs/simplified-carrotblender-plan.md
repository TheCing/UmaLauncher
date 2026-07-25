# Plan: Update-resilient CarrotBlender (forward raw payloads, decrypt launcher-side)

Status: **not started** — reference design for later. Written 2026-07-01.

## Motivation

CarrotBlender keeps breaking on game updates because it hooks *game-code-specific*
crypto methods whose class/offset change between builds. This session alone we
chased the response hook from `Convert.FromBase64String` → `CryptoStream.Read`
→ `RijndaelManagedTransform.TransformBlock`/`TransformFinalBlock`.

The insight (from `~/Dev/Heaven/decoder.py`) is that the API payload is
**self-decrypting** once you have the raw network body plus the device udid, so
CarrotBlender does not actually need the crypto hooks at all. If it just forwards
the raw (still-encrypted) request/response bodies and the launcher decrypts them,
the only hooks left are at the HTTP/body layer, which changes with the *Unity
version*, not with routine content patches — far more stable.

## The wire format (from Heaven's decoder.py — VERIFY before building)

```
base64( AES_CBC( u32_len[4] + msgpack_payload + PKCS7_padding, key, iv ) + key[32] )
```

- After base64-decode: `ciphertext || key`, where **key = last 32 bytes**.
- **iv = udid[:16]** — the locally-generated device id; stable per install.
- After AES-CBC decrypt: strip the leading 4-byte length header, then msgpack.
- This mirrors what the launcher already does in `unpack()` (which strips `[4:]`
  and msgpack-unpacks) — the only new parts are "split off the trailing key" and
  "iv comes from udid".

### Open questions to confirm first (cheap to verify)
1. **Is the iv really constant (= udid[:16]) across all responses?** Re-enable
   the `[diag]` logging of the per-response IV in CarrotBlender's `CreateDecryptor`
   hook and confirm every IV is identical. If so, it's the udid and we can hardcode
   the source. If IVs vary, the scheme is more complex and this plan needs revising.
2. **Does the key really travel in the payload (last 32 bytes)?** Compare the key
   CarrotBlender captures from `CreateDecryptor` against the last 32 bytes of the
   base64-decoded body. If they match, the launcher can extract the key itself and
   CarrotBlender never needs to send it.
3. **Same scheme for requests and responses?** decoder.py documents one format;
   confirm the request direction uses the same (it may use a different iv or no
   trailing key). The current `CryptoStream.Write` request hook already yields
   request *plaintext*, so requests may be able to stay as-is (msg type 3).

## Target architecture

```
Game (Unity)                         CarrotBlender (thin)          UmaLauncher
------------                         --------------------          -----------
HTTP response body (base64) ──hook──> forward raw bytes ──UDP──> decrypt(body, udid)
HTTP request  body (base64) ──hook──> forward raw bytes ──UDP──> (as today: type 3)
udid (captured once) ───────────────> forward once ─────UDP──> store as iv source
```

CarrotBlender shrinks to: **one response-body hook, one request-body hook, one
udid capture.** No `CreateDecryptor`, no `TransformBlock`/`TransformFinalBlock`,
no `FromBase64String`, no `CryptoStream` hooks.

## CarrotBlender changes (`~/Dev/CarrotBlender/examples/hello_hachimi/src/lib.rs`)

1. **Pick the stable body hook.** The raw base64 body is what crosses the network.
   Hook the Unity HTTP layer where the full body is available as a single buffer:
   - Response: `UnityWebRequest`/`DownloadHandler` text or raw-bytes getter
     (e.g. `DownloadHandlerBuffer.GetData`/`get_text`), OR the game's own API
     client method that receives the response string.
   - Request: `UploadHandlerRaw` data / the API client's send method.
   - These are engine-level and stable across content patches. Exact names need a
     one-time metadata dump of the current build (Il2CppDumper) to pin down.
   - Fallback if a clean single-buffer hook isn't found: keep hooking
     `Convert.FromBase64String` for the response (it *is* the base64 decode of the
     body) — but that's the fragile one that already broke once, so prefer the HTTP
     layer.
2. **Forward raw bytes** using the existing framing helpers. Reuse the current
   type scheme; add:
   - type `9` = raw response body (full), `10`/`11` = raw response multipart
     header/chunk (parallel to 0/4/5 and 6/7/8), OR just reuse 0/4/5 since those
     already mean "encrypted body the launcher must decrypt" — the only change is
     the launcher decrypts with udid+appended-key instead of a separately-sent
     key/iv.
   - Keep type 3 (request) as-is if requests still decode the current way.
3. **Capture the udid once.** Options, easiest first:
   - Read it from a request header/body the game sends (CarrotBlender already sees
     request plaintext via the Write hook — the udid/`device_id` is typically in
     there). Send it to the launcher as a new one-shot message type (e.g. `12 =
     udid`).
   - Or hook the game's udid getter once.
4. **Delete** the `CreateDecryptor`, `TransformBlock`, `TransformFinalBlock`,
   `CryptoStream.Read/Write`(response) hooks and their statics/accumulators
   (`DECRYPTOR_PTRS`, `RESPONSE_ACC`, `TRANSFORM_*_ORIG`). Keep the request path.

## UmaLauncher changes (`umalauncher/carrotjuicer.py`)

1. **Add a udid-aware decrypt** mirroring Heaven's `decoder.py`:
   ```python
   def decrypt_payload(body: bytes, udid: bytes) -> object:
       raw = base64.b64decode(body)           # if CB forwards base64; skip if raw
       ciphertext, key = raw[:-32], raw[-32:]
       iv = udid[:16]
       plain = AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext)
       plain = unpad(plain, 16)               # PKCS7
       return msgpack.unpackb(plain[4:], strict_map_key=False)  # strip u32 len
   ```
   (Confirm whether CB sends base64 or already-base64-decoded bytes, and whether
   the length header / padding handling matches `unpack()`.)
2. **Store the udid** when the new udid message (type 12) arrives; hold it on the
   `CarrotJuicer` instance. Gate response handling until it's known.
3. **Route the raw-body message type** into `decrypt_payload(...)` →
   `handle_response(obj, is_json=True)`. This replaces the current key/IV/data
   assembly (types 0/1/2) and the decrypted-response path (types 6/7/8) with a
   single raw-body path.
4. **Remove** the now-dead branches: the type 1/2 key/IV handling, the
   `encrypted_data` assembly, and the 6/7/8 decrypted-response handlers (or keep
   6/7/8 briefly for a transition period).

## Migration / compatibility

- Bump a protocol version so a new launcher rejects an old CarrotBlender (and vice
  versa) with a clear message instead of silently mis-decoding.
- Consider keeping the current working hooks in place behind a feature flag for one
  release so a bad guess on the HTTP hook name doesn't brick capture.

## Risks / caveats

- **Finding the stable HTTP hook still needs a metadata dump** of the current build
  once. The payoff is it should then survive content patches; the risk is picking a
  method that's inlined or itself unstable.
- If the iv is *not* the udid (open question 1), this whole simplification doesn't
  hold and we stay with the crypto-transform hooks.
- udid capture timing: must arrive before the first response we care about, or we
  buffer early responses until it's known.

## Relationship to the mitmproxy alternative

Same decrypt math (`decoder.py`) also enables a **no-injection** proxy path
(mitmproxy + system proxy + cert), which Heaven's "method B" uses. That avoids the
game DLL entirely but adds a system-wide cert/proxy burden and TLS-pinning risk.
This plan is the middle ground: keep a *thin* injector for capture, move decryption
(the stable part) into the launcher.

## Reference files

- `~/Dev/Heaven/decoder.py` — the payload wire format + a working Python decoder.
- `~/Dev/Heaven/tt_capture.py`, `discover_addon.py` — the mitmproxy capture path.
- `~/Dev/CarrotBlender/examples/hello_hachimi/src/lib.rs` — current hooks.
- `umalauncher/carrotjuicer.py` — `unpack()`, the UDP loop, `handle_response()`.
