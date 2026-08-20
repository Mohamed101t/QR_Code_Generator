from typing import Any
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity
from lib.features.qr_generator.domain.repositories.qr_repository_interface import IQRRepository


class GenerateQRCodeUseCase:
    """حالة استخدام: إنشاء رمز الـ QR"""

    def __init__(self, repository: IQRRepository):
        self.repository = repository

    def execute(self, entity: QRCodeEntity) -> Any:
        if not entity.is_valid():
            raise ValueError("المحتوى المدخل غير صالح أو فارغ.")

        return self.repository.generate_qr(entity)