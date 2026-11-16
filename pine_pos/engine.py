"""ERPNext POS EDC Swiper Terminal Integration (Pine Labs / Plutus / Razorpay POS)."""

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class POSPaymentIntent:
    pos_invoice_number: str
    edc_terminal_id: str
    amount_inr: float
    cashier_id: str
    payment_mode: str  # CREDIT_CARD, DEBIT_CARD, UPI_EDC, EMI
    timestamp_utc: str


@dataclass
class EDCTransactionResult:
    pos_invoice_number: str
    terminal_rrn: str          # Retrieval Reference Number
    auth_code: str
    card_last_4_digits: Optional[str]
    card_network: Optional[str]  # VISA, MASTERCARD, RUPAY
    amount_settled: float
    is_successful: bool
    status: str                 # APPROVED, DECLINED, TIMEOUT_CANCELLED


@dataclass
class POSShiftClosingSummary:
    shift_id: str
    cashier_id: str
    total_pos_sales_count: int
    gross_card_sales_amount: float
    gross_upi_sales_amount: float
    total_terminal_settled_inr: float
    is_shift_reconciled: bool


class PineLabsPOSGatewayEngine:
    """Manages cloud-to-EDC device payment intents, terminal charge responses, and cash drawer reconciliations."""

    def create_payment_intent(
        self,
        invoice_no: str,
        terminal_id: str,
        amount: float,
        cashier: str,
        mode: str = "CREDIT_CARD"
    ) -> POSPaymentIntent:
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        return POSPaymentIntent(
            pos_invoice_number=invoice_no,
            edc_terminal_id=terminal_id,
            amount_inr=round(amount, 2),
            cashier_id=cashier,
            payment_mode=mode,
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        )

    def process_edc_callback(
        self,
        intent: POSPaymentIntent,
        bank_rrn: str,
        auth_code: str,
        card_last4: str,
        network: str,
        is_approved: bool
    ) -> EDCTransactionResult:
        status = "APPROVED" if is_approved else "DECLINED_BY_ISSUING_BANK"

        return EDCTransactionResult(
            pos_invoice_number=intent.pos_invoice_number,
            terminal_rrn=bank_rrn,
            auth_code=auth_code,
            card_last_4_digits=card_last4,
            card_network=network,
            amount_settled=intent.amount_inr if is_approved else 0.0,
            is_successful=is_approved,
            status=status
        )

    def reconcile_pos_shift(
        self,
        shift_id: str,
        cashier: str,
        transactions: List[EDCTransactionResult]
    ) -> POSShiftClosingSummary:
        successful = [t for t in transactions if t.is_successful]
        card_sales = sum(t.amount_settled for t in successful if t.card_network in ("VISA", "MASTERCARD", "RUPAY"))
        upi_sales = sum(t.amount_settled for t in successful if t.card_network == "UPI")
        total_settled = card_sales + upi_sales

        return POSShiftClosingSummary(
            shift_id=shift_id,
            cashier_id=cashier,
            total_pos_sales_count=len(successful),
            gross_card_sales_amount=round(card_sales, 2),
            gross_upi_sales_amount=round(upi_sales, 2),
            total_terminal_settled_inr=round(total_settled, 2),
            is_shift_reconciled=True
        )
