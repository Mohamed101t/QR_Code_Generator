import unittest
from lib.features.qr_generator.data.datasources.qr_datasource import QRLocalDataSource
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity, QRContentType


class TestQRSecurity(unittest.TestCase):

    def setUp(self):
        self.datasource = QRLocalDataSource()

    def test_malicious_script_payload(self):
        payload = "<script>alert('XSS')</script> ; DROP TABLE Users; --"
        entity = QRCodeEntity(content=payload, content_type=QRContentType.TEXT)

        # التأكد من عدم انهيار المحرك ومعالجة السلسلة النصية كـ String آمن
        try:
            img = self.datasource.generate(entity)
            self.assertIsNotNone(img)
        except Exception as e:
            self.fail(f"Security processing failed on raw string input: {e}")

    def test_large_payload(self):
        large_payload = "A" * 2000
        entity = QRCodeEntity(content=large_payload, content_type=QRContentType.TEXT)
        img = self.datasource.generate(entity)
        self.assertIsNotNone(img)


if __name__ == "__main__":
    unittest.main()