# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "pine_pos"
app_title = "Erpnext Pos Pine Labs Payment Gateway"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Pos Pine Labs Payment Gateway for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/pine_pos/css/pine_pos.bundle.css"
app_include_js = "/assets/pine_pos/js/pine_pos.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "pine_pos.engine.on_document_submit",
        "on_cancel": "pine_pos.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "pine_pos.engine.daily_scheduled_sync"
    ]
}
