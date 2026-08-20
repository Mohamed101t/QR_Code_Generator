from typing import Any
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity
from lib.features.qr_generator.domain.repositories.qr_repository_interface import IQRRepository
from lib.features.qr_generator.data.datasources.qr_datasource import QRLocalDataSource


class QRRepositoryImpl(IQRRepository):
    """تنفيذ المستودع الذي يربط بين الـ Domain و الـ Datasource"""

    def __init__(self, datasource: QRLocalDataSource):
        self.datasource = datasource

    def generate_qr(self, entity: QRCodeEntity) -> Any:
        return self.datasource.generate(entity)

    def save_qr_code(self, image_data: Any, save_path: str) -> bool:
        return self.datasource.save_to_disk(image_data, save_path)

    def print_qr_code(self, image_data: Any) -> bool:
        return self.datasource.print_image(image_data)