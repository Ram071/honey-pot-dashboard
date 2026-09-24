from datetime import datetime, timezone

from flask import Flask, request

from database import add_event, init_db

app = Flask(__name__)


@app.before_request
def log_request():
    """Log request metadata without recording request bodies or credentials."""
    timestamp = datetime.now(timezone.utc).isoformat()
    source_ip = request.remote_addr or "unknown"
    method = request.method
    path = request.path
    user_agent = request.headers.get("User-Agent", "")

    add_event(
        timestamp=timestamp,
        ip=source_ip,
        method=method,
        path=path,
        user_agent=user_agent,
    )


@app.route("/", methods=["GET", "POST"])
def home():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Honeypot</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>This is a local laboratory web server.</p>
    </body>
    </html>
    """


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        return """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Admin Login</title>
        </head>
        <body>
            <h1>Login failed</h1>
            <p>The username or password was not accepted.</p>
            <p>No submitted credentials were stored.</p>
        </body>
        </html>
        """, 401

    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Admin Login</title>
    </head>
    <body>
        <h1>Administrator Login</h1>

        <form method="post" action="/admin">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" autocomplete="off">

            <br><br>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" autocomplete="off">

            <br><br>

            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """


@app.route("/wp-admin", methods=["GET", "POST"])
def wp_admin():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>WordPress Admin</title>
    </head>
    <body>
        <h1>WordPress Administration</h1>
        <p>This endpoint is part of the local honeypot.</p>
    </body>
    </html>
    """


@app.route("/phpmyadmin", methods=["GET", "POST"])
def phpmyadmin():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>phpMyAdmin</title>
    </head>
    <body>
        <h1>phpMyAdmin</h1>
        <p>This endpoint is part of the local honeypot.</p>
    </body>
    </html>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <p>This endpoint is part of the local honeypot.</p>
    </body>
    </html>
    """


@app.route("/robots.txt", methods=["GET", "POST"])
def robots():
    return "User-agent: *\nDisallow: /admin\nDisallow: /wp-admin\n", 200, {
        "Content-Type": "text/plain; charset=utf-8"
    }


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8080, debug=False)
