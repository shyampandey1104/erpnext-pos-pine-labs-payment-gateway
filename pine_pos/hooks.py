# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "pine_pos"
app_title = "Erpnext Pos Pine Labs Payment Gateway"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Pos Pine Labs Payment Gateway - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/pine_pos/css/pine_pos.bundle.css"
app_include_js = "/assets/pine_pos/js/pine_pos.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Pos Pine Labs Payment Gateway Entry": {
        "validate": "pine_pos.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "pine_pos.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "pine_pos.tasks.hourly_sync"
    ],
    "daily": [
        "pine_pos.tasks.daily_reconciliation"
    ],
    "weekly": [
        "pine_pos.tasks.weekly_digest"
    ]
}
