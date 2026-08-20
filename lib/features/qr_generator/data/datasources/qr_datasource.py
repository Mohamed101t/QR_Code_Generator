import sys
import qrcode
from PIL import Image, ImageDraw, ImageOps
from lib.features.qr_generator.domain.entities.qr_code_entity import QRCodeEntity, QRDotStyle


class QRLocalDataSource:
    """مصدر البيانات لإنشاء وتشكيل الرمز مع قص حواف الخلفية"""

    def generate(self, entity: QRCodeEntity) -> Image.Image:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=12,
            border=4,
        )
        qr.add_data(entity.content)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        box_size = qr.box_size
        border = qr.border
        width = (len(matrix) + 2 * border) * box_size
        height = width

        # إنشاء الخلفية الشفافة مؤقتاً لتسهيل قص الحواف
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 1. رسم بطاقة الخلفية مع الحواف المحددة
        if entity.card_radius > 0:
            draw.rounded_rectangle(
                [0, 0, width, height],
                radius=entity.card_radius,
                fill=entity.back_color,
            )
        else:
            draw.rectangle([0, 0, width, height], fill=entity.back_color)

        # 2. رسم نقاط ومربعات الرمز الداخلية
        for r, row in enumerate(matrix):
            for c, val in enumerate(row):
                if val:
                    x1 = (c + border) * box_size
                    y1 = (r + border) * box_size
                    x2 = x1 + box_size
                    y2 = y1 + box_size

                    if entity.style == QRDotStyle.ROUNDED:
                        draw.rounded_rectangle(
                            [x1, y1, x2, y2],
                            radius=box_size // 3,
                            fill=entity.fill_color,
                        )
                    elif entity.style == QRDotStyle.CIRCLE:
                        draw.ellipse([x1, y1, x2, y2], fill=entity.fill_color)
                    else:
                        draw.rectangle([x1, y1, x2, y2], fill=entity.fill_color)

        return img.convert("RGB")

    def save_to_disk(self, image: Image.Image, save_path: str) -> bool:
        try:
            image.save(save_path, format="PNG")
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def print_image(self, image: Image.Image) -> bool:
        try:
            from PyQt6.QtCore import QSize
            from PyQt6.QtGui import QImage, QPainter
            from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
            from PyQt6.QtWidgets import QApplication

            temp_path = "temp_print.png"
            image.save(temp_path)

            app = QApplication.instance() or QApplication(sys.argv)
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer)

            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                painter = QPainter(printer)
                qt_image = QImage(temp_path)

                rect = painter.viewport()
                size = QSize(qt_image.width(), qt_image.height())
                size.scale(rect.size(), 1)
                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(qt_image.rect())

                painter.drawImage(0, 0, qt_image)
                painter.end()
                return True
            return False
        except Exception as e:
            print(f"Error printing image: {e}")
            return False