import unittest
from lib.core.localization.localization_service import LocalizationService
from lib.features.qr_generator.data.datasources.qr_datasource import QRLocalDataSource
from lib.features.qr_generator.data.repositories.qr_repository_impl import QRRepositoryImpl
from lib.features.qr_generator.domain.usecases.generate_qr_uc import GenerateQRCodeUseCase
from lib.features.qr_generator.domain.usecases.print_qr_uc import PrintQRCodeUseCase
from lib.features.qr_generator.domain.usecases.save_qr_uc import SaveQRCodeUseCase
from lib.features.qr_generator.presentation.providers.qr_provider import QRNotifier


class TestE2EFlow(unittest.TestCase):

    def test_full_application_flow(self):
        # 1. تهيئة المحرك وربط الطبقات (Dependency Injection)
        ds = QRLocalDataSource()
        repo = QRRepositoryImpl(ds)
        gen_uc = GenerateQRCodeUseCase(repo)
        save_uc = SaveQRCodeUseCase(repo)
        print_uc = PrintQRCodeUseCase(repo)
        loc = LocalizationService("ar")

        notifier = QRNotifier(gen_uc, save_uc, print_uc, loc)

        # 2. تنفيذ توليد رمز QR كامل
        success, err = notifier.generate_qr(
            content="E2E Test Success",
            content_type_index=0,
            fill_color="#123456",
            back_color="#FFFFFF",
            style_index=1,
            card_radius=10,
        )

        # 3. التحقق من اكتمال التوليد وتوفر الصورة في الحالة العامة
        self.assertTrue(success)
        self.assertEqual(err, "")
        self.assertIsNotNone(notifier.state.current_image)


if __name__ == "__main__":
    unittest.main()