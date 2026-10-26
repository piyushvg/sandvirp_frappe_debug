app_name = "sandvirp_debug"
app_title = "Sandvirp Debug"
app_publisher = "Sandvirp"
app_description = "Log failed API requests for local replay"
app_email = "piyushs.work@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "sandvirp_debug",
# 		"logo": "/assets/sandvirp_debug/logo.png",
# 		"title": "Sandvirp Debug",
# 		"route": "/sandvirp_debug",
# 		"has_permission": "sandvirp_debug.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sandvirp_debug/css/sandvirp_debug.css"
# app_include_js = "/assets/sandvirp_debug/js/sandvirp_debug.js"

# include js, css files in header of web template
# web_include_css = "/assets/sandvirp_debug/css/sandvirp_debug.css"
# web_include_js = "/assets/sandvirp_debug/js/sandvirp_debug.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sandvirp_debug/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "sandvirp_debug/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "sandvirp_debug.utils.jinja_methods",
# 	"filters": "sandvirp_debug.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sandvirp_debug.install.before_install"
# after_install = "sandvirp_debug.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sandvirp_debug.uninstall.before_uninstall"
# after_uninstall = "sandvirp_debug.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sandvirp_debug.utils.before_app_install"
# after_app_install = "sandvirp_debug.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sandvirp_debug.utils.before_app_uninstall"
# after_app_uninstall = "sandvirp_debug.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sandvirp_debug.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"sandvirp_debug.tasks.all"
# 	],
# 	"daily": [
# 		"sandvirp_debug.tasks.daily"
# 	],
# 	"hourly": [
# 		"sandvirp_debug.tasks.hourly"
# 	],
# 	"weekly": [
# 		"sandvirp_debug.tasks.weekly"
# 	],
# 	"monthly": [
# 		"sandvirp_debug.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "sandvirp_debug.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "sandvirp_debug.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "sandvirp_debug.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sandvirp_debug.utils.before_request"]
# after_request = ["sandvirp_debug.utils.after_request"]

# Job Events
# ----------
# before_job = ["sandvirp_debug.utils.before_job"]
# after_job = ["sandvirp_debug.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"sandvirp_debug.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

