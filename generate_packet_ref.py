"""Generate a packet reference from training log .gz files."""
import os
import json
import gzip
import sys

os.environ['IS_UL_GLOBAL'] = '1'

LOG_DIR = os.path.join(os.path.dirname(__file__), 'umalauncher', 'appdata', 'training_logs')

def explore(obj, path='', catalog=None):
    if catalog is None:
        catalog = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            full = f'{path}.{k}' if path else k
            if isinstance(v, dict): vtype = 'object'
            elif isinstance(v, list): vtype = 'array'
            elif v is None: vtype = 'null'
            elif isinstance(v, bool): vtype = 'bool'
            elif isinstance(v, int): vtype = 'int'
            elif isinstance(v, float): vtype = 'float'
            elif isinstance(v, str): vtype = 'string'
            else: vtype = type(v).__name__

            if full not in catalog:
                catalog[full] = {'types': set(), 'samples': set(), 'count': 0, 'null_count': 0}
            catalog[full]['types'].add(vtype)
            catalog[full]['count'] += 1
            if v is None:
                catalog[full]['null_count'] += 1
            elif not isinstance(v, (dict, list)) and len(catalog[full]['samples']) < 5:
                catalog[full]['samples'].add(str(v)[:60])

            if isinstance(v, dict):
                explore(v, full, catalog)
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                explore(v[0], full + '[]', catalog)
    return catalog


def main():
    gz_files = sorted([f for f in os.listdir(LOG_DIR) if f.endswith('.gz')])
    if not gz_files:
        print("No .gz files found in", LOG_DIR)
        return

    catalog = {}
    req_count = 0
    resp_count = 0
    req_top = {}
    resp_top = {}
    run_names = []

    for fname in gz_files:
        fpath = os.path.join(LOG_DIR, fname)
        run_names.append(fname.replace('.gz', ''))
        with gzip.open(fpath, 'rb') as f:
            packets = json.loads(f'[{f.read().decode("utf-8")}]')
        for p in packets:
            d = p.get('_direction', -1)
            if d == 0:
                req_count += 1
                for k in p:
                    if k != '_direction':
                        req_top[k] = req_top.get(k, 0) + 1
            elif d == 1:
                resp_count += 1
                for k in p:
                    if k != '_direction':
                        resp_top[k] = resp_top.get(k, 0) + 1
            explore(p, '', catalog)

    total = req_count + resp_count
    lines = []
    lines.append('# Uma Musume Packet Reference')
    lines.append('')
    lines.append(f'Generated from **{total}** packets ({req_count} requests, {resp_count} responses) across **{len(gz_files)}** training runs (Global).')
    lines.append('')
    lines.append('Runs analyzed:')
    for name in run_names:
        lines.append(f'- {name}')
    lines.append('')

    # Top-level request keys
    lines.append('---')
    lines.append('')
    lines.append('## Top-Level Request Keys')
    lines.append('')
    lines.append('| Key | Type | Occurrences |')
    lines.append('|-----|------|-------------|')
    for k in sorted(req_top.keys()):
        info = catalog.get(k, {})
        types = ', '.join(sorted(info.get('types', set())))
        lines.append(f'| `{k}` | {types} | {req_top[k]}/{req_count} |')

    # Top-level response keys
    lines.append('')
    lines.append('## Top-Level Response Keys')
    lines.append('')
    lines.append('| Key | Type | Occurrences |')
    lines.append('|-----|------|-------------|')
    for k in sorted(resp_top.keys()):
        info = catalog.get(k, {})
        types = ', '.join(sorted(info.get('types', set())))
        lines.append(f'| `{k}` | {types} | {resp_top[k]}/{resp_count} |')

    # Nested keys grouped by top-level parent
    sections = {}
    for path in sorted(catalog.keys()):
        if '.' not in path:
            continue
        top = path.split('.')[0]
        if top == '_direction':
            continue
        if top not in sections:
            sections[top] = []
        sections[top].append(path)

    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## Nested Key Reference')
    lines.append('')

    for section in sorted(sections.keys()):
        paths = sections[section]
        lines.append(f'### `{section}`')
        lines.append('')
        lines.append('| Path | Type | Count | Sample Values |')
        lines.append('|------|------|-------|---------------|')
        for path in paths:
            info = catalog[path]
            types = ', '.join(sorted(info['types']))
            samples = ', '.join(sorted(info['samples']))
            if len(samples) > 80:
                samples = samples[:77] + '...'
            null_note = ''
            if info['null_count'] > 0:
                null_note = f' (null: {info["null_count"]}x)'
            lines.append(f'| `{path}` | {types}{null_note} | {info["count"]} | {samples} |')
        lines.append('')

    output = '\n'.join(lines)
    out_path = os.path.join(os.path.dirname(__file__), 'packet_reference.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f'Written {len(lines)} lines to {out_path}')
    print(f'{len(catalog)} unique key paths cataloged')


if __name__ == '__main__':
    main()
