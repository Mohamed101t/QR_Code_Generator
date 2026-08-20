from abc import ABC, abstractmethod
from typing import Any
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity


class IQRRepository(ABC):
    """عقد برمجي يحدد الوظائف المطلوبة لميزة الـ QR Code دون الاهتمام بكيفية التنفيذ"""

    @abstractmethod
    def generate_qr(self, entity: QRCodeEntity) -> Any:
        """توليد صورة الـ QR Code"""
        pass

    @abstractmethod
    def save_qr_code(self, image_data: Any, save_path: str) -> bool:
        """حفظ الصورة كملف PNG"""
        pass

    @abstractmethod
    def print_qr_code(self, image_data: Any) -> bool:
        """إرسال الصورة إلى الطابعة"""
        pass