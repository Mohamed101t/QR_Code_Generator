import unittest
from unittest.mock import MagicMock
from lib.features.qr_generator.presentation.providers.qr_provider import QRNotifier


class TestQRNotifierUnit(unittest.TestCase):

    def setUp(self):
        self.mock_gen_uc = MagicMock()
        self.mock_save_uc = MagicMock()
        self.mock_print_uc = MagicMock()
        self.mock_loc = MagicMock()
        self.notifier = QRNotifier(
            self.mock_gen_uc,
            self.mock_save_uc,
            self.mock_print_uc,
            self.mock_loc,
        )

    def test_format_as_clean_card(self):
        raw_input = "محمد طارق\nالوظيفة: مبرمج\nالموقع: https://example.com"
        result = self.notifier.format_as_clean_card(raw_input)

        self.assertIn("=== بطاقة معلومات: محمد طارق ===", result)
        self.assertIn("🔹 الوظيفة: مبرمج", result)
        self.assertIn("🔹 الموقع: https://example.com", result)


if __name__ == "__main__":
    unittest.main()