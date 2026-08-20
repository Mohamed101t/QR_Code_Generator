from dataclasses import dataclass
from enum import Enum


class QRContentType(Enum):
    TEXT = "text"              # نص عادي وبسيط
    INFO_CARD = "info_card"    # بطاقة معلومات منسقة تلقائياً
    URL = "url"
    IMAGE_URL = "image_url"
    VIDEO_URL = "video_url"


class QRDotStyle(Enum):
    SQUARE = "square"
    ROUNDED = "rounded"
    CIRCLE = "circle"


@dataclass
class QRCodeEntity:
    content: str
    content_type: QRContentType
    fill_color: str = "black"
    back_color: str = "white"
    style: QRDotStyle = QRDotStyle.SQUARE
    card_radius: int = 0

    def is_valid(self) -> bool:
        return bool(self.content and self.content.strip())