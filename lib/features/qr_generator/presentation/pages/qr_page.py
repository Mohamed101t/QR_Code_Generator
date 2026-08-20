from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
from PIL import Image

from lib.core.theme.app_theme import AppTheme
from lib.features.qr_generator.presentation.providers.qr_provider import QRNotifier


class QRGeneratorPage(ctk.CTk):

    def __init__(self, notifier: QRNotifier):
        super().__init__()

        self.notifier = notifier
        self.notifier.add_listener(self.on_state_changed)

        self.temp_qr_path = "temp_qr_display.png"
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"

        self.geometry("960x740")
        self.minsize(860, 640)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- الشريط العلوي ---
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 0), sticky="ew")

        self.lang_option = ctk.CTkOptionMenu(
            self.top_frame,
            values=["العربية", "English", "中文", "Français", "Русский", "हिन्दी"],
            command=self.on_language_change,
            width=140,
        )
        self.lang_option.pack(side="right")

        # --- قسم التحكم والتنسيق ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

        self.label_type = ctk.CTkLabel(self.input_frame, font=("Arial", 14, "bold"))
        self.label_type.pack(padx=10, pady=(10, 2), anchor="w")

        self.type_option = ctk.CTkOptionMenu(
            self.input_frame, values=[], command=self.on_type_changed
        )
        self.type_option.pack(padx=10, pady=2, fill="x")

        self.label_content = ctk.CTkLabel(self.input_frame, font=("Arial", 14, "bold"))
        self.label_content.pack(padx=10, pady=(10, 2), anchor="w")

        # ملصق توضيحي يبسط الأمر للمستخدم غير التقني
        self.label_hint = ctk.CTkLabel(
            self.input_frame,
            text="",
            font=("Arial", 11),
            text_color="#888888",
            justify="left",
        )
        self.label_hint.pack(padx=10, pady=(0, 2), anchor="w")

        self.entry_data = ctk.CTkTextbox(self.input_frame, height=110)
        self.entry_data.pack(padx=10, pady=2, fill="x")
        self.entry_data.bind("<KeyRelease>", lambda e: self.auto_refresh_qr())

        # 1. شكل نقاط الرمز
        self.label_style = ctk.CTkLabel(
            self.input_frame, text="شكل نقاط الرمز الداخلي:", font=("Arial", 13, "bold")
        )
        self.label_style.pack(padx=10, pady=(8, 2), anchor="w")

        self.style_option = ctk.CTkOptionMenu(
            self.input_frame,
            values=["مربعات حادة (Default)", "حواف دائرية (Rounded)", "نقاط دائرية (Circles)"],
            command=lambda _: self.auto_refresh_qr(),
        )
        self.style_option.pack(padx=10, pady=2, fill="x")

        # 2. انحناء حواف خلفية الكارت
        self.label_bg_radius = ctk.CTkLabel(
            self.input_frame, text="انحناء حواف خلفية الكارت:", font=("Arial", 13, "bold")
        )
        self.label_bg_radius.pack(padx=10, pady=(8, 2), anchor="w")

        self.slider_bg_radius = ctk.CTkSlider(
            self.input_frame,
            from_=0,
            to=60,
            number_of_steps=12,
            command=lambda _: self.auto_refresh_qr(),
        )
        self.slider_bg_radius.set(0)
        self.slider_bg_radius.pack(padx=10, pady=2, fill="x")

        # 3. الألوان
        self.label_customs = ctk.CTkLabel(self.input_frame, font=("Arial", 13, "bold"))
        self.label_customs.pack(padx=10, pady=(8, 2), anchor="w")

        self.colors_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        self.colors_frame.pack(padx=10, pady=2, fill="x")

        self.btn_fill_color = ctk.CTkButton(
            self.colors_frame, text="لون الرمز", command=self.choose_fill_color, width=120
        )
        self.btn_fill_color.pack(side="left", padx=(0, 10))

        self.btn_back_color = ctk.CTkButton(
            self.colors_frame, text="خلفية الرمز", command=self.choose_back_color, width=120
        )
        self.btn_back_color.pack(side="left")

        self.btn_generate = ctk.CTkButton(
            self.input_frame,
            command=self.generate_qr,
            fg_color=AppTheme.PRIMARY_COLOR,
            font=("Arial", 14, "bold"),
        )
        self.btn_generate.pack(padx=10, pady=15, fill="x")

        # --- قسم العرض والطباعة ---
        self.display_frame = ctk.CTkFrame(self)
        self.display_frame.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

        self.qr_label = ctk.CTkLabel(self.display_frame, width=280, height=280)
        self.qr_label.pack(padx=10, pady=20, expand=True)

        self.btn_save = ctk.CTkButton(
            self.display_frame, command=self.save_png, state="disabled"
        )
        self.btn_save.pack(padx=10, pady=8, fill="x")

        self.btn_print = ctk.CTkButton(
            self.display_frame,
            command=self.print_qr,
            fg_color=AppTheme.PRINT_COLOR,
            state="disabled",
        )
        self.btn_print.pack(padx=10, pady=8, fill="x")

        self.update_texts()

    def on_type_changed(self, choice):
        """تجهيز إرشادات ونصائح الإدخال التلقائي للنوع المختار"""
        types = self.notifier.loc.get_text("types")
        selected_index = types.index(choice) if choice in types else 0

        if selected_index == 1:  # معلومات شخصية / بطاقة أعمال
            self.label_hint.configure(
                text="اكتب الاسم في السطر الأول، وفي الأسطر التالية ضَع: الوظيفة: المدير / الهاتف: 010... / رابط الصورة"
            )
            if not self.entry_data.get("1.0", "end-1c").strip():
                sample = "محمد طارق\nالوظيفة: مبرمج ورسام\nالهاتف: 0100000000\nالموقع: https://example.com"
                self.entry_data.delete("1.0", "end")
                self.entry_data.insert("1.0", sample)
        else:
            self.label_hint.configure(text="")

        self.auto_refresh_qr()

    def choose_fill_color(self):
        color = colorchooser.askcolor(title="اختر لون الرمز")[1]
        if color:
            self.fill_color = color
            self.auto_refresh_qr()

    def choose_back_color(self):
        color = colorchooser.askcolor(title="اختر لون الخلفية")[1]
        if color:
            self.back_color = color
            self.auto_refresh_qr()

    def auto_refresh_qr(self):
        data = self.entry_data.get("1.0", "end-1c").strip()
        if data:
            self.generate_qr(show_error=False)

    def on_language_change(self, choice):
        mapping = {
            "العربية": "ar",
            "English": "en",
            "中文": "zh",
            "Français": "fr",
            "Русский": "ru",
            "हिन्दी": "hi",
        }
        code = mapping.get(choice, "ar")
        self.notifier.change_language(code)

    def update_texts(self):
        loc = self.notifier.loc
        self.title(loc.get_text("title"))
        self.label_type.configure(text=loc.get_text("select_type"))

        types = loc.get_text("types")
        self.type_option.configure(values=types)
        if not self.type_option.get() or self.type_option.get() not in types:
            self.type_option.set(types[0])

        self.label_content.configure(text=loc.get_text("enter_data"))
        self.btn_generate.configure(text=loc.get_text("btn_generate"))
        self.label_customs.configure(text=loc.get_text("qr_customs"))
        self.btn_fill_color.configure(text=loc.get_text("fill_color"))
        self.btn_back_color.configure(text=loc.get_text("back_color"))

        if self.notifier.state.current_image is None:
            self.qr_label.configure(text=loc.get_text("qr_placeholder"))

        self.btn_save.configure(text=loc.get_text("btn_save"))
        self.btn_print.configure(text=loc.get_text("btn_print"))

    def on_state_changed(self, state):
        self.update_texts()

        if state.current_image is not None:
            state.current_image.save(self.temp_qr_path)
            ctk_img = ctk.CTkImage(
                light_image=Image.open(self.temp_qr_path),
                dark_image=Image.open(self.temp_qr_path),
                size=(260, 260),
            )
            self.qr_label.configure(image=ctk_img, text="")
            self.btn_save.configure(state="normal")
            self.btn_print.configure(state="normal")

    def generate_qr(self, show_error: bool = True):
        data = self.entry_data.get("1.0", "end-1c").strip()
        types = self.notifier.loc.get_text("types")
        selected_index = (
            types.index(self.type_option.get())
            if self.type_option.get() in types
            else 0
        )

        styles_list = ["مربعات حادة (Default)", "حواف دائرية (Rounded)", "نقاط دائرية (Circles)"]
        selected_style_index = (
            styles_list.index(self.style_option.get())
            if self.style_option.get() in styles_list
            else 0
        )

        card_radius = int(self.slider_bg_radius.get())

        success, err = self.notifier.generate_qr(
            content=data,
            content_type_index=selected_index,
            fill_color=self.fill_color,
            back_color=self.back_color,
            style_index=selected_style_index,
            card_radius=card_radius,
        )
        if not success and show_error:
            messagebox.showwarning(
                self.notifier.loc.get_text("err_title"),
                err or self.notifier.loc.get_text("err_msg"),
            )

    def save_png(self):
        loc = self.notifier.loc
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png")],
            title=loc.get_text("save_dialog_title"),
        )
        if file_path:
            if self.notifier.save_qr(file_path):
                messagebox.showinfo(
                    loc.get_text("success_title"), loc.get_text("success_msg")
                )

    def print_qr(self):
        self.notifier.print_qr()