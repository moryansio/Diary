import customtkinter as ctk
import gettext
import os
from logic import (
    add_entry,
    search_entry,
    search_by_keyword,
    search_by_date_range,
    show_all_entries,
    delete_entries_by_date,
    delete_all_entries
)

def set_language_env(lang_code):
    locale_path = os.path.join(os.path.dirname(__file__), "locales")
    lang = gettext.translation("messages", localedir=locale_path, languages=[lang_code], fallback=True)
    lang.install()
    return lang.gettext

class DiaryGUI(ctk.CTk):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.language = "ru"
        self._ = set_language_env(self.language)
        self.date_format = "%Y-%m-%d"

        self.title("Diary App")
        self.geometry("1000x700")

        self.create_tabs()

    def create_tabs(self):
        self.main_area = ctk.CTkTabview(self, width=950, height=600)
        self.main_area.pack(padx=20, pady=20)

        self.main_area.add(self._("Добавить"))
        self.main_area.add(self._("Поиск"))
        self.main_area.add(self._("Удалить"))
        self.main_area.add(self._("Все записи"))
        self.main_area.add(self._("Настройки"))

        self.setup_add_tab()
        self.setup_search_tab()
        self.setup_delete_tab()
        self.setup_show_tab()
        self.setup_settings_tab()


        self.set_date_format(self.date_format)

    def set_date_format(self, fmt):
        self.date_format = fmt
        if hasattr(self, "date_entry"):
            self.update_placeholders()

    def update_placeholders(self):
        placeholders = {
            self.date_entry: self.get_date_placeholder(),
            self.search_date: self.get_date_placeholder(),
            self.delete_date: self.get_date_placeholder(),
            self.range_start: self._("С ") + self.get_date_placeholder(),
            self.range_end: self._("По ") + self.get_date_placeholder()
        }
        for entry, text in placeholders.items():
            if entry.get() == "":
                entry.configure(placeholder_text=text)

    def get_date_placeholder(self):
        return self.date_format.replace("%Y", "2025").replace("%m", "10").replace("%d", "10")

    def setup_add_tab(self):
        tab = self.main_area.tab(self._("Добавить"))
        form_frame = ctk.CTkFrame(tab, fg_color="transparent")
        form_frame.pack(pady=30)

        self.date_entry = ctk.CTkEntry(form_frame, placeholder_text=self.get_date_placeholder(), width=300)
        self.text_entry = ctk.CTkEntry(form_frame, placeholder_text=self._("Текст записи"), width=600)
        submit_btn = ctk.CTkButton(form_frame, text=self._("Добавить"), command=self.handle_add)
        self.result_label = ctk.CTkLabel(form_frame, text="", text_color="green")

        self.date_entry.pack(pady=10)
        self.text_entry.pack(pady=10)
        submit_btn.pack(pady=10)
        self.result_label.pack(pady=10)

    def handle_add(self):
        result = add_entry(self.conn, self.date_entry.get(), self.text_entry.get(), self.date_format)
        self.result_label.configure(text=result)
        self.date_entry.delete(0, "end")
        self.text_entry.delete(0, "end")
        self.update_placeholders()

    def setup_search_tab(self):
        tab = self.main_area.tab(self._("Поиск"))
        search_frame = ctk.CTkFrame(tab, fg_color="transparent")
        search_frame.pack(pady=20)

        self.search_date = ctk.CTkEntry(search_frame, placeholder_text=self.get_date_placeholder(), width=300)
        btn_date = ctk.CTkButton(search_frame, text=self._("Поиск по дате"), command=self.handle_search_date)

        self.search_keyword = ctk.CTkEntry(search_frame, placeholder_text=self._("Ключевое слово"), width=300)
        btn_keyword = ctk.CTkButton(search_frame, text=self._("Поиск по слову"), command=self.handle_search_keyword)

        self.range_start = ctk.CTkEntry(search_frame, placeholder_text=self._("С ") + self.get_date_placeholder(), width=200)
        self.range_end = ctk.CTkEntry(search_frame, placeholder_text=self._("По ") + self.get_date_placeholder(), width=200)
        btn_range = ctk.CTkButton(search_frame, text=self._("Поиск по диапазону"), command=self.handle_search_range)

        self.search_result = ctk.CTkTextbox(tab, width=850, height=400)

        self.search_date.pack(pady=10)
        btn_date.pack(pady=5)
        self.search_keyword.pack(pady=10)
        btn_keyword.pack(pady=5)
        self.range_start.pack(pady=10)
        self.range_end.pack(pady=5)
        btn_range.pack(pady=5)
        self.search_result.pack(pady=20)

    def handle_search_date(self):
        result = search_entry(self.conn, self.search_date.get(), self.date_format)
        self.search_result.delete("0.0", "end")
        self.search_result.insert("0.0", result)

    def handle_search_keyword(self):
        result = search_by_keyword(self.conn, self.search_keyword.get())
        self.search_result.delete("0.0", "end")
        self.search_result.insert("0.0", result)

    def handle_search_range(self):
        result = search_by_date_range(self.conn, self.range_start.get(), self.range_end.get(), self.date_format)
        self.search_result.delete("0.0", "end")
        self.search_result.insert("0.0", result)

    def setup_delete_tab(self):
        tab = self.main_area.tab(self._("Удалить"))
        self.delete_date = ctk.CTkEntry(tab, placeholder_text=self.get_date_placeholder(), width=300)
        self.delete_result = ctk.CTkLabel(tab, text="", text_color="red")
        btn_date = ctk.CTkButton(tab, text=self._("Удалить по дате"), command=self.handle_delete_date)
        btn_all = ctk.CTkButton(tab, text=self._("Удалить все"), command=self.handle_delete_all)

        self.delete_date.pack(pady=10)
        btn_date.pack(pady=5)
        btn_all.pack(pady=5)
        self.delete_result.pack(pady=10)

    def handle_delete_date(self):
        result = delete_entries_by_date(self.conn, self.delete_date.get(), self.date_format)
        self.delete_result.configure(text=result)
        self.delete_date.delete(0, "end")
        self.update_placeholders()

    def handle_delete_all(self):
        result = delete_all_entries(self.conn)
        self.delete_result.configure(text=result)

    def setup_show_tab(self):
        tab = self.main_area.tab(self._("Все записи"))
        self.show_result = ctk.CTkTextbox(tab, width=850, height=500)
        btn = ctk.CTkButton(tab, text=self._("Показать"), command=self.handle_show_all)
        btn.pack(pady=10)
        self.show_result.pack(pady=10)

    def handle_show_all(self):
        result = show_all_entries(self.conn)
        self.show_result.delete("0.0", "end")
        self.show_result.insert("0.0", result)

    def setup_settings_tab(self):
        tab = self.main_area.tab(self._("Настройки"))
        sidebar = ctk.CTkFrame(tab, width=250)
        sidebar.pack(side="left", fill="y", padx=20, pady=20)

        self.options_panel = ctk.CTkFrame(tab, fg_color="transparent")
        self.options_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(sidebar, text=self._("Настройки"), font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(10, 20))

        for label, command in [
            (self._("Выбрать тему"), self.show_theme_options),
            (self._("Выбрать язык"), self.show_language_options),
            (self._("Выбрать формат даты"), self.show_date_format_options),
            (self._("Сбросить настройки"), self.reset_settings)
        ]:
            section = ctk.CTkLabel(sidebar, text=label, font=ctk.CTkFont(size=14))
            section.pack(pady=(0, 5))
            btn = ctk.CTkButton(sidebar, text=label, command=command)
            btn.pack(pady=(0, 15), fill="x")

    def show_theme_options(self):
        self.clear_options_panel()
        label = ctk.CTkLabel(self.options_panel, text=self._("Выберите тему:"))
        label.pack(pady=10)

        themes = [("Light", self._("Светлая")), ("Dark", self._("Тёмная")), ("System", self._("Системная"))]
        for theme_code, theme_label in themes:
            btn = ctk.CTkButton(self.options_panel, text=theme_label, command=lambda t=theme_code: self.set_theme(t))
            btn.pack(pady=5)

    def show_language_options(self):
        self.clear_options_panel()
        label = ctk.CTkLabel(self.options_panel, text=self._("Выберите язык:"))
        label.pack(pady=10)
        for code, name in [("ru", "Русский"), ("en", "English")]:
            btn = ctk.CTkButton(self.options_panel, text=name, command=lambda c=code: self.set_language(c))
            btn.pack(pady=5)

    def show_date_format_options(self):
        self.clear_options_panel()
        label = ctk.CTkLabel(self.options_panel, text=self._("Выберите формат даты:"))
        label.pack(pady=10)
        formats = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"]
        for fmt in formats:
            btn = ctk.CTkButton(self.options_panel, text=fmt, command=lambda f=fmt: self.set_date_format(f))
            btn.pack(pady=5)

    def set_language(self, lang):
        self.language = lang
        self._ = set_language_env(lang)
        self.clear_options_panel()
        label = ctk.CTkLabel(self.options_panel,
                             text=self._("Язык установлен: ") + ("Русский" if lang == "ru" else "English"))
        label.pack(pady=20)
        self.rebuild_ui()

    def set_theme(self, theme):
        ctk.set_appearance_mode(theme)

    def reset_settings(self):
        self.language = "ru"
        self._ = set_language_env("ru")
        self.date_format = "%Y-%m-%d"
        ctk.set_appearance_mode("System")
        self.clear_options_panel()
        label = ctk.CTkLabel(self.options_panel, text=self._("Настройки сброшены к значениям по умолчанию."))
        label.pack(pady=20)
        self.rebuild_ui()

    def clear_options_panel(self):
        for widget in self.options_panel.winfo_children():
            widget.destroy()

    def rebuild_ui(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_tabs()
