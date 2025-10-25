import os
import json
from flask import Flask, jsonify, request, render_template, send_from_directory

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
LOGS_PATH = os.path.join(ROOT, 'logs', 'test_system_structured.jsonl')


def load_alerts(limit=100):
    alerts = []
    try:
        if os.path.exists(LOGS_PATH):
            with open(LOGS_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        alerts.append(obj)
                    except Exception:
                        # skip malformed lines
                        continue
    except Exception:
        return []
    # return newest first
    return list(reversed(alerts))[:limit]


def make_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/alerts')
    def api_alerts():
        try:
            limit = int(request.args.get('limit', '100'))
        except ValueError:
            limit = 100
        alerts = load_alerts(limit)
        # normalize a lightweight representation if needed
        lightweight = []
        for i, a in enumerate(alerts):
            lightweight.append({
                'id': a.get('id', f'alert-{i}'),
                'timestamp': a.get('timestamp'),
                'source': a.get('source', a.get('plugin', 'unknown')),
                'severity': a.get('severity', 'low'),
                'message': a.get('message', str(a.get('event', a)))
            })
        return jsonify(lightweight)

    @app.route('/api/stats')
    def api_stats():
        alerts = load_alerts(1000)
        total = len(alerts)
        by_sev = {'low': 0, 'medium': 0, 'high': 0}
        for a in alerts:
            sev = a.get('severity', '').lower()
            if sev.startswith('h'):
                by_sev['high'] += 1
            elif sev.startswith('m'):
                by_sev['medium'] += 1
            else:
                by_sev['low'] += 1
        return jsonify({'total_alerts': total, 'by_severity': by_sev})

    @app.route('/api/logs')
    def api_logs():
        try:
            limit = int(request.args.get('limit', '100'))
        except ValueError:
            limit = 100
        alerts = load_alerts(limit)
        return jsonify(alerts)

    @app.route('/api/alerts/<alert_id>/ack', methods=['POST'])
    def ack_alert(alert_id):
        # Placeholder: integrate with real plugin/engine to ack/handle an alert
        return jsonify({'status': 'ok', 'id': alert_id})

    return app


app = make_app()


if __name__ == '__main__':
    # dev server: open http://127.0.0.1:5000
    app.run(host='127.0.0.1', port=5000, debug=True)
