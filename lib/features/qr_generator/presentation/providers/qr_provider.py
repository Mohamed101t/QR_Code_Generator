from typing import Optional, Callable
from PIL import Image

from lib.core.localization.localization_service import LocalizationService
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity, QRContentType, QRDotStyle
from lib.features.qr_generator.domain.usecases.generate_qr_uc import GenerateQRCodeUseCase
from lib.features.qr_generator.domain.usecases.save_qr_uc import SaveQRCodeUseCase
from lib.features.qr_generator.domain.usecases.print_qr_uc import PrintQRCodeUseCase


class QRState:
    def __init__(self, current_image: Optional[Image.Image] = None):
        self.current_image = current_image


class QRNotifier:
    def __init__(
        self,
        generate_uc: GenerateQRCodeUseCase,
        save_uc: SaveQRCodeUseCase,
        print_uc: PrintQRCodeUseCase,
        localization_service: LocalizationService,
    ):
        self._generate_uc = generate_uc
        self._save_uc = save_uc
        self._print_uc = print_uc
        self.loc = localization_service

        self.state = QRState()
        self._listeners = []

    def add_listener(self, callback: Callable):
        self._listeners.append(callback)

    def _notify_listeners(self):
        for callback in self._listeners:
            callback(self.state)

    def change_language(self, lang_code: str):
        self.loc.set_language(lang_code)
        self._notify_listeners()

    def format_as_clean_card(self, raw_data: str) -> str:
        """تحويل البيانات إلى بطاقة معلومات عربية سهلة وواضحة بدون رموز مارك داون"""
        lines = [line.strip() for line in raw_data.strip().split("\n") if line.strip()]
        if not lines:
            return raw_data

        # السطر الأول: الاسم / العنوان الرئيسي
        title = lines[0]
        body_lines = lines[1:]

        card_text = f"=== بطاقة معلومات: {title} ===\n\n"

        for line in body_lines:
            if line.startswith("http://") or line.startswith("https://"):
                card_text += f"🔗 الرابط: {line}\n"
            elif ":" in line or "：" in line:
                key, val = line.split(":", 1) if ":" in line else line.split("：", 1)
                card_text += f"🔹 {key.strip()}: {val.strip()}\n"
            else:
                card_text += f"▫️ {line}\n"

        card_text += "\n=========================="
        return card_text

    def generate_qr(
        self,
        content: str,
        content_type_index: int,
        fill_color: str = "black",
        back_color: str = "white",
        style_index: int = 0,
        card_radius: int = 0,
    ) -> tuple[bool, str]:

        type_mapping = [
            QRContentType.TEXT,
            QRContentType.INFO_CARD,
            QRContentType.URL,
            QRContentType.IMAGE_URL,
            QRContentType.VIDEO_URL,
        ]
        selected_type = (
            type_mapping[content_type_index]
            if content_type_index < len(type_mapping)
            else QRContentType.TEXT
        )

        final_content = content
        # تحويل المحتوى تلقائياً إذا كان نوعه بطاقة معلومات إلى تنسيق صافٍ
        if selected_type == QRContentType.INFO_CARD and content.strip():
            final_content = self.format_as_clean_card(content)

        styles = [QRDotStyle.SQUARE, QRDotStyle.ROUNDED, QRDotStyle.CIRCLE]
        selected_style = styles[style_index] if style_index < len(styles) else QRDotStyle.SQUARE

        entity = QRCodeEntity(
            content=final_content,
            content_type=selected_type,
            fill_color=fill_color,
            back_color=back_color,
            style=selected_style,
            card_radius=card_radius,
        )

        try:
            image = self._generate_uc.execute(entity)
            self.state = QRState(current_image=image)
            self._notify_listeners()
            return True, ""
        except Exception as e:
            return False, str(e)

    def save_qr(self, save_path: str) -> bool:
        if self.state.current_image is None:
            return False
        return self._save_uc.execute(self.state.current_image, save_path)

    def print_qr(self) -> bool:
        if self.state.current_image is None:
            return False
        return self._print_uc.execute(self.state.current_image)