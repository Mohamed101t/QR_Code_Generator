from typing import Any
from lib.features.qr_generator.domain.repositories.qr_repository_interface import IQRRepository


class PrintQRCodeUseCase:
    """حالة استخدام: إرسال الـ QR إلى الطابعة"""

    def __init__(self, repository: IQRRepository):
        self.repository = repository

    def execute(self, image_data: Any) -> bool:
        if image_data is None:
            raise ValueError("لا توجد صورة طباعة متوفرة.")

        return self.repository.print_qr_code(image_data)