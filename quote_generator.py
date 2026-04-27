import json
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "quotes_history.json"

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator - Генератор цитат")
        self.root.geometry("800x650")
        self.root.resizable(True, True)
        
        # Предопределённые цитаты
        self.default_quotes = [
            {"text": "Будь тем изменением, которое хочешь увидеть в мире", "author": "Махатма Ганди", "theme": "мотивация"},
            {"text": "Жизнь - это то, что с тобой происходит, пока ты строишь планы", "author": "Джон Леннон", "theme": "жизнь"},
            {"text": "Единственный способ делать великую работу - любить то, что ты делаешь", "author": "Стив Джобс", "theme": "работа"},
            {"text": "Знание - сила", "author": "Фрэнсис Бэкон", "theme": "знание"},
            {"text": "Воображение важнее знания", "author": "Альберт Эйнштейн", "theme": "творчество"},
            {"text": "Не бойся совершенства - тебе его не достичь", "author": "Сальвадор Дали", "theme": "мотивация"},
            {"text": "Простое действие лучше тысячи намерений", "author": "Джон Барроуз", "theme": "действие"},
            {"text": "Счастье - это путь, а не пункт назначения", "author": "Будда", "theme": "счастье"},
            {"text": "Ты поступаешь правильно, только если можешь спать спокойно", "author": "Элеонора Рузвельт", "theme": "жизнь"},
            {"text": "Сложнее всего начать действовать, остальное зависит от упорства", "author": "Пабло Пикассо", "theme": "мотивация"},
            {"text": "Вера в себя - вот секрет успеха", "author": "Чарли Чаплин", "theme": "успех"},
            {"text": "Делай сегодня то, что другие не хотят, завтра будешь жить так, как другие не могут", "author": "Джаред Лето", "theme": "мотивация"},
        ]
        
        # Текущий список цитат (предустановленные + добавленные пользователем)
        self.quotes = []
        self.history = []
        
        self.load_data()
        self.create_widgets()
        self.update_author_filter()
        self.update_theme_filter()
    
    def create_widgets(self):
        # === Панель генерации ===
        generate_frame = ttk.LabelFrame(self.root, text="Генерация цитаты", padding=10)
        generate_frame.pack(fill="x", padx=10, pady=5)
        
        self.generate_btn = ttk.Button(generate_frame, text="🎲 Сгенерировать случайную цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=10)
        
        # === Отображение текущей цитаты ===
        quote_frame = ttk.LabelFrame(self.root, text="Текущая цитата", padding=10)
        quote_frame.pack(fill="x", padx=10, pady=5)
        
        self.quote_text_label = tk.Text(quote_frame, height=4, wrap=tk.WORD, font=("Arial", 11), relief=tk.SUNKEN, bg="#f5f5f5")
        self.quote_text_label.pack(fill="x", padx=5, pady=5)
        
        self.quote_info_label = ttk.Label(quote_frame, text="Автор: — | Тема: —", font=("Arial", 9, "italic"))
        self.quote_info_label.pack()
        
        # === Панель фильтрации ===
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация истории", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.filter_author_combo = ttk.Combobox(filter_frame, width=20)
        self.filter_author_combo.grid(row=0, column=1, padx=5, pady=2)
        self.filter_author_combo.bind("«ComboboxSelected»", lambda e: self.filter_history())
        
        ttk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.filter_theme_combo = ttk.Combobox(filter_frame, width=20)
        self.filter_theme_combo.grid(row=0, column=3, padx=5, pady=2)
        self.filter_theme_combo.bind("«ComboboxSelected»", lambda e: self.filter_history())
        
        self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.filter_history)
        self.filter_btn.grid(row=0, column=4, padx=10, pady=2)
        
        self.reset_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.reset_filter)
        self.reset_filter_btn.grid(row=0, column=5, padx=5, pady=2)
        
        # === История цитат ===
        history_frame = ttk.LabelFrame(self.root, text="История цитат", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Таблица истории
        columns = ("text", "author", "theme", "date")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        
        self.history_tree.heading("text", text="Цитата")
        self.history_tree.heading("author", text="Автор")
        self.history_tree.heading("theme", text="Тема")
        self.history_tree.heading("date", text="Дата/Время")
        
        self.history_tree.column("text", width=350)
        self.history_tree.column("author", width=120)
        self.history_tree.column("theme", width=100)
        self.history_tree.column("date", width=140)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # === Панель добавления новой цитаты ===
        add_frame = ttk.LabelFrame(self.root, text="Добавить свою цитату", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(add_frame, text="Текст цитаты:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.new_quote_text = ttk.Entry(add_frame, width=50)
        self.new_quote_text.grid(row=0, column=1, columnspan=3, padx=5, pady=2, sticky="ew")
        
        ttk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.new_quote_author = ttk.Entry(add_frame, width=20)
        self.new_quote_author.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        ttk.Label(add_frame, text="Тема:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.new_quote_theme = ttk.Entry(add_frame, width=20)
        self.new_quote_theme.grid(row=1, column=3, padx=5, pady=2, sticky="w")
        
        self.add_quote_btn = ttk.Button(add_frame, text="➕ Добавить цитату", command=self.add_quote)
        self.add_quote_btn.grid(row=2, column=0, columnspan=4, pady=5)
        
        # === Кнопка очистки истории ===
        clear_frame = ttk.Frame(self.root)
        clear_frame.pack(fill="x", padx=10, pady=5)
        
        self.clear_history_btn = ttk.Button(clear_frame, text="🗑️ Очистить историю", command=self.clear_history)
        self.clear_history_btn.pack(side="left", padx=5)
        
        # Информационная метка
        self.info_label = ttk.Label(self.root, text="Нажмите кнопку для генерации цитаты")
        self.info_label.pack(pady=5)
    
    def update_author_filter(self):
        """Обновление списка авторов в фильтре"""
        authors = sorted(set([q["author"] for q in self.quotes]))
        self.filter_author_combo["values"] = [""] + authors
    
    def update_theme_filter(self):
        """Обновление списка тем в фильтре"""
        themes = sorted(set([q["theme"] for q in self.quotes]))
        self.filter_theme_combo["values"] = [""] + themes
    
    def generate_quote(self):
        """Генерация случайной цитаты"""
        if not self.quotes:
            messagebox.showerror("Ошибка", "Нет доступных цитат!")
            return
        
        quote = random.choice(self.quotes)
        
        # Отображение цитаты
        self.quote_text_label.delete(1.0, tk.END)
        self.quote_text_label.insert(1.0, f'"{quote["text"]}"')
        self.quote_info_label.config(text=f"Автор: {quote['author']} | Тема: {quote['theme']}")
        
        # Добавление в историю
        from datetime import datetime
        history_entry = {
            "text": quote["text"],
            "author": quote["author"],
            "theme": quote["theme"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.insert(0, history_entry)
        self.save_data()
        self.update_history_display()
        
        self.info_label.config(text=f"Сгенерирована цитата от {quote['author']}")
    
    def filter_history(self):
        """Фильтрация истории по автору и теме"""
        filter_author = self.filter_author_combo.get().strip()
        filter_theme = self.filter_theme_combo.get().strip()
        
        filtered = self.history.copy()
        
        if filter_author:
            filtered = [h for h in filtered if h["author"] == filter_author]
        
        if filter_theme:
            filtered = [h for h in filtered if h["theme"] == filter_theme]
        
        self.update_history_display(filtered)
        self.info_label.config(text=f"Найдено записей: {len(filtered)} (всего: {len(self.history)})")
    
    def reset_filter(self):
        """Сброс фильтрации"""
        self.filter_author_combo.set("")
        self.filter_theme_combo.set("")
        self.update_history_display()
        self.info_label.config(text=f"Фильтр сброшен. Всего записей: {len(self.history)}")
    
    def update_history_display(self, history_list=None):
        """Обновление отображения истории"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if history_list is None:
            history_list = self.history
        
        for entry in history_list:
            # Усечение длинных цитат для отображения
            text_display = entry["text"][:60] + "..." if len(entry["text"]) > 60 else entry["text"]
            self.history_tree.insert("", 0, values=(
                text_display,
                entry["author"],
                entry["theme"],
                entry["date"]
            ))
    
    def add_quote(self):
        """Добавление новой цитаты пользователем"""
        text = self.new_quote_text.get().strip()
        author = self.new_quote_author.get().strip()
        theme = self.new_quote_theme.get().strip()
        
        # Проверка на пустые строки
        if not text:
            messagebox.showerror("Ошибка", "Текст цитаты не может быть пустым!")
            return
        
        if not author:
            messagebox.showerror("Ошибка", "Укажите автора цитаты!")
            return
        
        if not theme:
            messagebox.showerror("Ошибка", "Укажите тему цитаты!")
            return
        
        new_quote = {
            "text": text,
            "author": author,
            "theme": theme
        }
        
        self.quotes.append(new_quote)
        self.save_data()
        
        # Обновление фильтров
        self.update_author_filter()
        self.update_theme_filter()
        
        # Очистка полей
        self.new_quote_text.delete(0, tk.END)
        self.new_quote_author.delete(0, tk.END)
        self.new_quote_theme.delete(0, tk.END)
        
        self.info_label.config(text=f"Цитата добавлена! Всего цитат: {len(self.quotes)}")
        messagebox.showinfo("Успех", "Новая цитата добавлена в коллекцию!")
    
    def clear_history(self):
        """Очистка истории цитат"""
        if not self.history:
            messagebox.showinfo("Информация", "История уже пуста!")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю цитат?"):
            self.history = []
            self.save_data()
            self.update_history_display()
            self.info_label.config(text="История очищена")
    
    def save_data(self):
        """Сохранение данных в JSON"""
        data = {
            "quotes": self.quotes,
            "history": self.history
        }
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def load_data(self):
        """Загрузка данных из JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.quotes = data.get("quotes", [])
                    self.history = data.get("history", [])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                self.quotes = []
                self.history = []
        
        # Если нет загруженных цитат или файл пуст, загружаем предопределённые
        if not self.quotes:
            self.quotes = self.default_quotes.copy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
