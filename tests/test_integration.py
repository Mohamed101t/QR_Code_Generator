import unittest
from PIL import Image
from lib.features.qr_generator.data.datasources.qr_datasource import QRLocalDataSource
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity, QRContentType, QRDotStyle


class TestQRIntegration(unittest.TestCase):

    def setUp(self):
        self.datasource = QRLocalDataSource()

    def test_generate_and_convert_image(self):
        entity = QRCodeEntity(
            content="Integration Test Data",
            content_type=QRContentType.TEXT,
            fill_color="#000000",
            back_color="#FFFFFF",
            style=QRDotStyle.ROUNDED,
            card_radius=20,
        )
        img = self.datasource.generate(entity)

        self.assertIsInstance(img, Image.Image)
        self.assertGreater(img.width, 0)
        self.assertGreater(img.height, 0)


if __name__ == "__main__":
    unittest.main()