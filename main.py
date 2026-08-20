import os
import sys

# إضافة المسار الحالي للنظام للتعرف على الموديولات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.core.theme.app_theme import AppTheme
from lib.core.localization.localization_service import LocalizationService

from lib.features.qr_generator.data.datasources.qr_datasource import QRLocalDataSource
from lib.features.qr_generator.data.repositories.qr_repository_impl import QRRepositoryImpl

from lib.features.qr_generator.domain.usecases.generate_qr_uc import GenerateQRCodeUseCase
from lib.features.qr_generator.domain.usecases.save_qr_uc import SaveQRCodeUseCase
from lib.features.qr_generator.domain.usecases.print_qr_uc import PrintQRCodeUseCase

from lib.features.qr_generator.presentation.providers.qr_provider import QRNotifier
from lib.features.qr_generator.presentation.pages.qr_page import QRGeneratorPage


def main():
    # 1. تهيئة Core Services
    AppTheme.setup_theme()
    localization_service = LocalizationService(default_lang="ar")

    # 2. تهيئة Data Layer
    datasource = QRLocalDataSource()
    repository = QRRepositoryImpl(datasource=datasource)

    # 3. تهيئة Use Cases (Domain Layer)
    generate_uc = GenerateQRCodeUseCase(repository=repository)
    save_uc = SaveQRCodeUseCase(repository=repository)
    print_uc = PrintQRCodeUseCase(repository=repository)

    # 4. تهيئة State Provider / Controller (Presentation Layer)
    qr_notifier = QRNotifier(
        generate_uc=generate_uc,
        save_uc=save_uc,
        print_uc=print_uc,
        localization_service=localization_service,
    )

    # 5. تشغيل الواجهة الرئيسية
    app = QRGeneratorPage(notifier=qr_notifier)
    app.mainloop()


if __name__ == "__main__":
    main()