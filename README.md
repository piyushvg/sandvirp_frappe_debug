### Sandvirp Debug

Log failed API requests for local replay

### What it does

Every failed `/api/*` request (4xx/5xx except 401/429) is saved as an **API Failure Log**
(path, HTTP method, user, status, exception type, error message, request args, whitelisted headers, response body).
Sensitive keys (`password`, `pwd`, `token`, `secret`, `api_key`, `otp`, `aadhaar`, `pan`...) are masked as `***`.
Logs older than 30 days are auto-cleared (Log Settings). System Manager only.

Uninstalling the app removes the hook, the DocType and all logged data.

### Installation

```bash
bench get-app git@github.com:piyushvg/sandvirp_frappe_debug.git --branch main
bench --site <site> install-app sandvirp_debug
```

If `tabAPI Failure Log` is missing after install (stale module cache), run `bench --site <site> migrate`.

### Config (site_config.json)

```bash
# pause logging without uninstalling
bench --site <site> set-config disable_api_failure_log 1
# log only selected endpoints
bench --site <site> set-config api_failure_log_paths '["/api/method/community_circle_app."]' --parse
```

### Debug a failure locally

1. Prod Desk → `/app/api-failure-log` → open row → **Copy Export JSON** (5xx rows include the Error Log traceback when available).
2. Save to a file, e.g. `~/log.json`. Fill any `***` values you need.
3. Replay in-process on a local site (same user, same args; `breakpoint()` works; rolled back unless `commit`):

```bash
bench --site <local-site> execute sandvirp_debug.api_failure_log.replay --kwargs '{"json_path": "/Users/me/log.json"}'
# options: "as_user": "x@y.com", "commit": true, or "name": "<log name>" for a local log
```

Supports `/api/method/*`, `/api/v2/method/*` and `/api/resource/*` (GET/POST/PUT/DELETE).
Anything else: **Copy as cURL** and fire it at your local server.

Data-dependent bugs need matching records locally (restore a prod backup).

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/sandvirp_debug
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
