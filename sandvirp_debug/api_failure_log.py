"""Log failed /api/* requests and replay them locally.

Kill switch:   bench --site X set-config disable_api_failure_log 1
Limit paths:   bench --site X set-config api_failure_log_paths '["/api/method/myapp."]' --parse
Replay:        bench --site X execute sandvirp_debug.api_failure_log.replay --kwargs '{"json_path": "/path/log.json"}'
"""

import json
import re
import shlex
from urllib.parse import unquote

import frappe
from frappe.client import get_list
from frappe.utils import add_to_date, strip_html

SKIP_STATUS = (401, 429)
MAX_BODY = 20_000
MASK = "***"
SENSITIVE_KEY = re.compile(
	r"pass|pwd|secret|token|api_key|apikey|otp|cookie|aadhaar|aadhar|\bpan\b|pan_no|pan_number", re.I
)
HEADER_WHITELIST = ("User-Agent", "Content-Type", "Origin", "Referer", "X-Requested-With", "Accept")


def log_failed_request(request, response):
	"""after_request hook. Must never raise."""
	try:
		if not _should_log(request, response):
			return

		body = _parse_response(response)
		doc = frappe.get_doc(
			{
				"doctype": "API Failure Log",
				"method": request.method,
				"path": request.path[:1000],
				"status_code": response.status_code,
				"user": frappe.session.user if frappe.db.exists("User", frappe.session.user) else None,
				"ip": getattr(frappe.local, "request_ip", None),
				"exc_type": body.get("exc_type") or _v2_error_type(body),
				"error_message": _error_message(body),
				"request_args": _dumps(_mask(_request_args(request))),
				"query_string": _mask_query(request.query_string.decode(errors="replace")),
				"headers": _dumps(_headers(request)),
				"response_body": _dumps(_mask(body))[:MAX_BODY]
				if body
				else response.get_data(as_text=True)[:MAX_BODY],
			}
		)
		doc.insert(ignore_permissions=True)
		# request transaction was already rolled back by frappe.app; this commits only the log row
		frappe.db.commit()
	except Exception:
		frappe.logger("sandvirp_debug").exception("Failed to write API Failure Log")


def _should_log(request, response):
	if not response or response.status_code < 400 or response.status_code in SKIP_STATUS:
		return False
	if not frappe.db or frappe.conf.get("disable_api_failure_log"):
		return False
	if not (request.path.startswith("/api/") or frappe.form_dict.get("cmd")):
		return False
	if "sandvirp_debug.api_failure_log" in request.path:
		return False
	if paths := frappe.conf.get("api_failure_log_paths"):
		return any(request.path.startswith(p) for p in paths)
	return frappe.db.table_exists("API Failure Log")


def _request_args(request):
	args = dict(frappe.form_dict)
	for key, file in (request.files or {}).items():
		args[key] = f"<file: {file.filename}>"
	return args


def _mask(value):
	if isinstance(value, dict):
		return {k: MASK if SENSITIVE_KEY.search(str(k)) else _mask(v) for k, v in value.items()}
	if isinstance(value, list):
		return [_mask(v) for v in value]
	if isinstance(value, str) and value.startswith(("{", "[")):
		# form-encoded clients often send nested JSON as strings
		try:
			return json.dumps(_mask(json.loads(value)))
		except ValueError:
			return value
	return value


def _mask_query(query_string):
	return re.sub(
		r"([^&=]+)=([^&]*)",
		lambda m: f"{m[1]}={MASK}" if SENSITIVE_KEY.search(unquote(m[1])) else m[0],
		query_string,
	)


def _headers(request):
	headers = {h: request.headers.get(h) for h in HEADER_WHITELIST if request.headers.get(h)}
	headers.update({k: v for k, v in request.headers.items() if k.lower().startswith("x-frappe-")})
	headers.pop("X-Frappe-CSRF-Token", None)
	return headers


def _parse_response(response):
	try:
		body = json.loads(response.get_data(as_text=True))
		return body if isinstance(body, dict) else {}
	except ValueError:
		return {}


def _v2_error_type(body):
	errors = body.get("errors") or []
	return errors[0].get("type") if errors and isinstance(errors[0], dict) else None


def _error_message(body):
	parts = []
	for raw in json.loads(body.get("_server_messages") or "[]"):
		try:
			msg = json.loads(raw)
			parts.append(msg.get("message") if isinstance(msg, dict) else str(msg))
		except ValueError:
			parts.append(raw)
	for err in body.get("errors") or []:
		if isinstance(err, dict) and err.get("message"):
			parts.append(err["message"])
	if body.get("exception") and not parts:
		parts.append(str(body["exception"]).strip().splitlines()[-1])
	return strip_html("\n".join(p for p in parts if p))[:5000]


def _dumps(value):
	return json.dumps(value, indent=1, default=str)


def find_error_log(doc):
	"""5xx Error Logs are inserted deferred (no name at request time); match by time + exception title."""
	if doc.status_code < 500:
		return None
	filters = {
		"creation": ["between", [add_to_date(doc.creation, seconds=-5), add_to_date(doc.creation, minutes=5)]]
	}
	if doc.error_message:
		filters["method"] = ["like", f"%{doc.error_message.splitlines()[-1][:100]}%"]
	return frappe.db.get_value("Error Log", filters, "name", order_by="creation asc")


@frappe.whitelist()
def export(name):
	frappe.only_for("System Manager")
	doc = frappe.get_doc("API Failure Log", name)
	data = doc.as_dict(no_default_fields=True)
	data["name"] = doc.name
	data["creation"] = str(doc.creation)
	if error_log := doc.error_log or find_error_log(doc):
		data["error_log"] = error_log
		data["traceback"] = frappe.db.get_value("Error Log", error_log, "error")
	return data


@frappe.whitelist()
def as_curl(name, base_url="http://localhost:8000"):
	frappe.only_for("System Manager")
	doc = frappe.get_doc("API Failure Log", name)
	url = base_url.rstrip("/") + doc.path + (f"?{doc.query_string}" if doc.query_string else "")
	parts = [
		"curl",
		"-X",
		doc.method,
		shlex.quote(url),
		"-H",
		shlex.quote("Authorization: token <api_key>:<api_secret>"),
	]
	args = json.loads(doc.request_args or "{}")
	args.pop("cmd", None)
	if doc.method != "GET" and args:
		parts += [
			"-H",
			shlex.quote("Content-Type: application/json"),
			"--data",
			shlex.quote(json.dumps(args)),
		]
	return " ".join(parts)


def replay(name=None, json_path=None, as_user=None, commit=False):
	"""Re-run a logged request in-process so breakpoint()/pdb and full tracebacks work.

	Use on a LOCAL site. Rolls back unless commit=True.
	"""
	log = _load(name, json_path)
	user = as_user or log.get("user")
	if not user or not frappe.db.exists("User", user):
		print(f"User {user!r} not found locally, using Administrator")
		user = "Administrator"

	args = json.loads(log.get("request_args") or "{}")
	args.pop("cmd", None)
	masked = [k for k, v in args.items() if v == MASK]
	if masked:
		print(f"WARNING: masked args {masked} — pass real values by editing the JSON")

	method, path = log["method"], log["path"]
	print(f"Replaying {method} {path} as {user}\nargs: {_dumps(args)}")

	frappe.set_user(user)
	frappe.local.form_dict = frappe._dict(args)
	try:
		result = _dispatch(method, path, args)
		print("Result:", _dumps(result))
		if commit:
			frappe.db.commit()
		return result
	finally:
		if not commit:
			frappe.db.rollback()


def _load(name, json_path):
	if json_path:
		with open(json_path) as f:
			return frappe._dict(json.load(f))
	if name:
		return frappe._dict(frappe.get_doc("API Failure Log", name).as_dict())
	frappe.throw("Pass name or json_path")


def _dispatch(method, path, args):
	parts = [unquote(p) for p in path.strip("/").split("/")]
	# ["api", "method", cmd] | ["api", "v2", "method", cmd] | ["api", "v2", "method", doctype, method]
	if parts[1] == "v2":
		parts = [parts[0], *parts[2:]]
		if parts[1] == "document":
			parts[1] = "resource"
	kind, rest = parts[1], parts[2:]

	if kind == "method":
		if len(rest) == 2:
			doc = frappe.get_doc(rest[0], args.pop("name", None) or args.pop("docname"))
			return doc.run_method(rest[1], **args)
		cmd = frappe.override_whitelisted_method(rest[0])
		return frappe.call(frappe.get_attr(cmd), **args)

	if kind == "resource":
		doctype = rest[0]
		name = rest[1] if len(rest) > 1 else None
		if args.get("data") and isinstance(args["data"], str):
			args.update(json.loads(args.pop("data")))
		if not name:
			if method == "GET":
				return get_list(doctype, **{k: v for k, v in args.items() if k != "doctype"})
			if method == "POST":
				return frappe.get_doc({**args, "doctype": doctype}).insert().as_dict()
		elif method == "GET":
			return frappe.get_doc(doctype, name).as_dict()
		elif method == "PUT":
			doc = frappe.get_doc(doctype, name)
			doc.update(args)
			return doc.save().as_dict()
		elif method == "DELETE":
			return frappe.delete_doc(doctype, name)
		elif method == "POST" and args.get("run_method"):
			return frappe.get_doc(doctype, name).run_method(args.pop("run_method"), **args)

	frappe.throw(f"Replay not supported for {method} {path}; use as_curl instead")
