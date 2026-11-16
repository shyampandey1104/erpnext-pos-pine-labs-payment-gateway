import unittest
from pine_pos.engine import PineLabsPOSGatewayEngine

class TestPineLabsPOS(unittest.TestCase):
    def test_payment_intent_and_settlement(self):
        engine = PineLabsPOSGatewayEngine()

        intent = engine.create_payment_intent(
            invoice_no="POS-INV-2026-091",
            terminal_id="PL-EDC-MUM-01",
            amount=2599.0,
            cashier="cashier_rahul",
            mode="CREDIT_CARD"
        )
        self.assertEqual(intent.amount_inr, 2599.0)

        res = engine.process_edc_callback(
            intent=intent,
            bank_rrn="408819284112",
            auth_code="AUTH-9081",
            card_last4="4112",
            network="VISA",
            is_approved=True
        )
        self.assertTrue(res.is_successful)
        self.assertEqual(res.status, "APPROVED")
        self.assertEqual(res.amount_settled, 2599.0)

    def test_shift_reconciliation(self):
        engine = PineLabsPOSGatewayEngine()
        intent1 = engine.create_payment_intent("INV-1", "PL-01", 1000.0, "c1")
        intent2 = engine.create_payment_intent("INV-2", "PL-01", 500.0, "c1", mode="UPI")

        t1 = engine.process_edc_callback(intent1, "RRN-1", "A1", "1234", "VISA", True)
        t2 = engine.process_edc_callback(intent2, "RRN-2", "A2", "UPI", "UPI", True)

        summary = engine.reconcile_pos_shift("SHIFT-A-2026", "c1", [t1, t2])
        self.assertEqual(summary.gross_card_sales_amount, 1000.0)
        self.assertEqual(summary.gross_upi_sales_amount, 500.0)
        self.assertEqual(summary.total_terminal_settled_inr, 1500.0)
        self.assertTrue(summary.is_shift_reconciled)

if __name__ == "__main__":
    unittest.main()
