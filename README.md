# Honeypot Security Dashboard

A beginner-friendly cybersecurity laboratory project consisting of a small local Flask honeypot and a dark-themed security dashboard.

The honeypot records basic HTTP request metadata in a local SQLite database. The dashboard displays those events and automatically refreshes every five seconds.

This project is designed for controlled local cybersecurity practice.

## Project Purpose

The project demonstrates a few fundamental defensive-security concepts:

- Running a deliberately fake web service.
- Recording basic HTTP request metadata.
- Storing security events in SQLite.
- Viewing events through a simple security dashboard.
- Handling untrusted HTTP data safely.
- Using parameterized SQL queries.
- Keeping a laboratory service bound to the local machine.

The project does not capture submitted usernames, passwords, cookies, tokens, or other sensitive request data.

## Features

### Honeypot

The honeypot runs at:

`http://127.0.0.1:8080`

It provides these routes:

- `/`
- `/admin`
- `/wp-admin`
- `/phpmyadmin`
- `/login`
- `/robots.txt`

Every request is recorded with:

- Timestamp
- Source IP
- HTTP method
- Requested path
- User-Agent

The `/admin` endpoint provides a fake login form.

POST requests to `/admin` return a generic failed-login message. Submitted usernames and passwords are never stored or logged.

### Dashboard

The dashboard runs at:

`http://127.0.0.1:5000`

It displays:

- Total events
- Unique source IPs
- Honeypot status
- Event ID
- Timestamp
- Source IP
- HTTP method
- Requested path
- User-Agent

The page automatically refreshes every five seconds.

Database values displayed by the dashboard are HTML-escaped to prevent stored XSS through malicious User-Agent or path values.

## Project Structure

```text
honeypot-project/
├── honeypot.py
├── database.py
├── dashboard.py
├── requirements.txt
└── README.md
