from typing import Any
from lib.features.qr_generator.domain.repositories.qr_repository_interface import IQRRepository


class SaveQRCodeUseCase:
    """حالة استخدام: حفظ الـ QR كصورة PNG"""

    def __init__(self, repository: IQRRepository):
        self.repository = repository

    def execute(self, image_data: Any, save_path: str) -> bool:
        if not save_path:
            raise ValueError("مسار الحفظ غير محدد.")

        return self.repository.save_qr_code(image_data, save_path)