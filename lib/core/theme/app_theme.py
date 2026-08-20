import customtkinter as ctk

class AppTheme:
    """خدمة تهيئة وإدارة ألوان ومظهر التطبيق"""

    PRIMARY_COLOR = "#1f538d"
    PRINT_COLOR = "#2b8a3e"
    SECONDARY_COLOR = "#555555"

    @staticmethod
    def setup_theme():
        """ضبط النظام والمظهر الافتراضي"""
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")