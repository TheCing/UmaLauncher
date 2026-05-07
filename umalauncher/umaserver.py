import glob
import os

from flask import Flask, request, jsonify, send_file
from werkzeug.serving import make_server
from loguru import logger
import json
import util

domain = '127.0.0.1'
port = 3150

app = Flask(__name__)
threader = None


def _add_cors(response):
    # Local Hakuraku dev runs on a different port (typically 5173) so any
    # cross-origin fetch from there to us needs explicit CORS headers.
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


@app.route('/')
def index():
    return 'Hello World!'


def _find_latest_race_log():
    """Return absolute path to the most recently modified race JSON.

    Walks appdata/{GL|JP}/race_logs/** and picks the newest, ignoring the
    aggregated race_summary.json and any temp/repair artefacts.
    """
    base = util.get_appdata_region("race_logs")
    if not os.path.isdir(base):
        return None
    candidates = []
    for path in glob.glob(os.path.join(base, '**', '*.json'), recursive=True):
        name = os.path.basename(path)
        if name == 'race_summary.json':
            continue
        if name.endswith('.tmp') or name.startswith('race_unknown_') or name.startswith('Unknown-'):
            continue
        candidates.append(path)
    if not candidates:
        return None
    return max(candidates, key=os.path.getmtime)


@app.route('/last-race', methods=['GET', 'OPTIONS'])
def last_race():
    if request.method == 'OPTIONS':
        return _add_cors(app.make_response(('', 204)))
    path = _find_latest_race_log()
    if not path:
        return _add_cors(jsonify({'error': 'No race logs found'})), 404
    logger.info(f"Serving latest race log: {path}")
    response = send_file(path, mimetype='application/json')
    return _add_cors(response)

# @app.route('/open-skill-window', methods=['OPTIONS'])
# def open_skills_window_options():
#     return '', 200

@app.route('/open-skill-window', methods=['POST'])
def open_skills_window():
    global threader
    if threader.carrotjuicer:
        threader.carrotjuicer.open_skill_window = True

    return '', 200

@app.route('/helper-window-rect', methods=['POST'])
def helper_window_rect():
    global threader
    # Json is sent as text/plain in body.
    json_data = json.loads(request.data.decode('utf-8'))
    
    if threader.carrotjuicer:
        threader.carrotjuicer.last_browser_rect = json_data

    return '', 200

@app.route('/skills-window-rect', methods=['POST'])
def skills_window_rect():
    global threader
    # Json is sent as text/plain in body.
    json_data = json.loads(request.data.decode('utf-8'))
    
    if threader.carrotjuicer:
        threader.carrotjuicer.last_skills_rect = json_data

    return '', 200

@app.route('/topmost', methods=['POST'])
def topmost():
    global threader
    # Json is sent as text/plain in body.
    json_data = json.loads(request.data.decode('utf-8'))

    if threader.carrotjuicer:
        threader.carrotjuicer.set_browser_topmost(json_data)
    return '', 200



# Patcher-related
@app.route("/patcher-start", methods=['POST'])
def patcher_start():
    # Patcher has signaled that it has started.
    global threader

    if threader.umaserver:
        threader.umaserver.en_patch_started = True
    return '', 200

@app.route("/patcher-finish", methods=['POST'])
def patcher_finish():
    # Patcher has signaled that it has finished.
    global threader

    json_data = json.loads(request.data.decode('utf-8'))
    if threader.umaserver:
        threader.umaserver.en_patch_success.append(json_data.get('success', False))
        threader.umaserver.en_patch_error = json_data.get('error', "")

    return '', 200


class UmaServer():
    en_patch_success = []

    def __init__(self, incoming_threader):
        global threader
        self.server = None
        threader = incoming_threader

        self.reset_en_patch()
    
    def reset_en_patch(self):
        self.en_patch_started = False
        self.en_patch_success.clear()
        self.en_patch_error = ""

    def run_with_catch(self):
        try:
            self.run()
        except Exception:
            util.show_error_box("Critical Error", "Uma Launcher has encountered a critical error and will now close.")

    def run(self):
        logger.info("Starting server")
        self.server = make_server(domain, port, app)
        self.server.serve_forever()

    def stop(self):
        logger.info("Stopping server")
        if self.server:
            self.server.shutdown()
        logger.info("Server stopped")