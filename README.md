# ERPNext POS Pine Labs / EDC Card Terminal Payment Gateway

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![POS](https://img.shields.io/badge/Retail-Pine%20Labs%20%2F%20Razorpay%20POS-orange.svg)](https://frappe.io)

Hardware and cloud payment integration for ERPNext POS retail counters connecting Pine Labs Plutus and Razorpay POS Android EDC swipe terminals with real-time payment reconciliation.

## Features
- **Cloud-to-EDC Payment Push:** Sends transaction totals directly to the EDC counter terminal without manual key entry.
- **Card Tap/Chip/UPI Capture:** Captures Bank RRN, authorization codes, card networks (Visa/Mastercard/RuPay), and last-4 digits.
- **POS Shift Closing Reconciliation:** Automatically matches EDC payment batch settlement against POS Opening/Closing vouchers.

## Tests
```bash
python3 -m unittest discover tests
```
