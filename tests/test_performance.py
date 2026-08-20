import unittest
import time
from lib.features.qr_generator.data.datasources.qr_datasource import QRLocalDataSource
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity, QRContentType


class TestQRPerformance(unittest.TestCase):

    def test_generation_speed(self):
        datasource = QRLocalDataSource()
        entity = QRCodeEntity(content="Speed Test Content", content_type=QRContentType.TEXT)

        start_time = time.time()
        for _ in range(50):
            _ = datasource.generate(entity)
        total_time = time.time() - start_time

        print(f"\n[Performance] Time for 50 QR Generations: {total_time:.4f} seconds")
        self.assertLess(total_time, 2.0)  # اشتراط معالجة 50 رمزًا في أقل من ثانيتين


if __name__ == "__main__":
    unittest.main()