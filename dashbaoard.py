import socket

from flask import Flask, render_template_string

from database import get_events, init_db

app = Flask(__name__)

DASHBOARD_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="5">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Honeypot Security Dashboard</title>

    <style>
        :root {
            color-scheme: dark;
            --background: #070b10;
            --panel: #0d141c;
            --panel-border: #1c3445;
            --green: #39ff88;
            --cyan: #28d7fe;
            --text: #d7e2ea;
            --muted: #7e929f;
            --red: #ff5364;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 24px;
            background: var(--background);
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            margin-bottom: 6px;
            color: var(--green);
            text-shadow: 0 0 8px rgba(57, 255, 136, 0.35);
        }

        .subtitle {
            margin-top: 0;
            color: var(--muted);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(180px, 1fr));
            gap: 16px;
            margin: 24px 0;
        }

        .card {
            padding: 20px;
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.25);
        }

        .card-label {
            color: var(--muted);
            font-size: 0.85rem;
            text-transform: uppercase;
        }

        .card-value {
            margin-top: 10px;
            color: var(--cyan);
            font-size: 1.8rem;
            font-weight: bold;
        }

        .status-online {
            color: var(--green);
        }

        .status-offline {
            color: var(--red);
        }

        .table-container {
            overflow-x: auto;
            background: var(--panel);
            border: 1px solid var(--panel-border);
            border-radius: 8px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 900px;
        }

        th,
        td {
            padding: 12px 14px;
            text-align: left;
            border-bottom: 1px solid #172633;
            vertical-align: top;
        }

        th {
            color: var(--cyan);
            background: #101b25;
            position: sticky;
            top: 0;
        }

        tr:hover {
            background: #111c26;
        }

        td {
            word-break: break-word;
        }

        .empty {
            padding: 30px;
            text-align: center;
            color: var(--muted);
        }

        .refresh {
            margin-top: 12px;
            color: var(--muted);
            font-size: 0.8rem;
        }

        @media (max-width: 800px) {
            body {
                padding: 12px;
            }

            .stats {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>

<body>
<div class="container">
    <h1>HONEYPOT SECURITY DASHBOARD</h1>
    <p class="subtitle">Local laboratory request monitor</p>

    <section class="stats">
        <div class="card">
            <div class="card-label">Total Events</div>
            <div class="card-value">{{ total_events }}</div>
        </div>

        <div class="card">
            <div class="card-label">Unique Source IPs</div>
            <div class="card-value">{{ unique_ips }}</div>
        </div>

        <div class="card">
            <div class="card-label">Honeypot Status</div>
            <div class="card-value {{ status_class }}">{{ honeypot_status }}</div>
        </div>
    </section>

    <div class="table-container">
        {% if events %}
        <table>
            <thead>
                <tr>
                    <th>Event ID</th>
                    <th>Timestamp</th>
                    <th>Source IP</th>
                    <th>HTTP Method</th>
                    <th>Requested Path</th>
                    <th>User-Agent</th>
                </tr>
            </thead>
            <tbody>
                {% for event in events %}
                <tr>
                    <td>{{ event[0] | e }}</td>
                    <td>{{ event[1] | e }}</td>
                    <td>{{ event[2] | e }}</td>
                    <td>{{ event[3] | e }}</td>
                    <td>{{ event[4] | e }}</td>
                    <td>{{ event[5] | e }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
        <div class="empty">
            No honeypot events have been recorded yet.
        </div>
        {% endif %}
    </div>

    <div class="refresh">
        Dashboard automatically refreshes every 5 seconds.
    </div>
</div>
</body>
</html>
"""


def is_honeypot_running():
    """Check whether the local honeypot port is accepting connections."""
    try:
        with socket.create_connection(("127.0.0.1", 8080), timeout=0.5):
            return True
    except (ConnectionRefusedError, TimeoutError, OSError):
        return False


@app.route("/")
def dashboard():
    events = get_events()

    unique_ips = len({event[2] for event in events})
    honeypot_running = is_honeypot_running()

    return render_template_string(
        DASHBOARD_TEMPLATE,
        events=events,
        total_events=len(events),
        unique_ips=unique_ips,
        honeypot_status="RUNNING" if honeypot_running else "OFFLINE",
        status_class="status-online" if honeypot_running else "status-offline",
    )


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
