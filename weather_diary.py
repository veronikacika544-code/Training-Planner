
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "weather_data.json"

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("900x500")

        self.records = []
        self.load_data()

        # Поля ввода
        input_frame = tk.LabelFrame(root, text="Новая запись", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.date_entry = tk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.temp_entry = tk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Описание:").grid(row=0, column=4, sticky="e", padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame, width=25)
        self.desc_entry.grid(row=0, column=5, padx=5, pady=5)

        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="Осадки", variable=self.precip_var).grid(row=0, column=6, padx=5, pady=5)

        tk.Button(input_frame, text="Добавить запись", command=self.add_record, bg="lightgreen").grid(row=0, column=7, padx=10, pady=5)

        # Фильтры
        filter_frame = tk.LabelFrame(root, text="Фильтр", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5)
        self.filter_date_entry = tk.Entry(filter_frame, width=12)
        self.filter_date_entry.grid(row=0, column=1, padx=5)
        tk.Button(filter_frame, text="Применить", command=self.apply_filters).grid(row=0, column=2, padx=5)

        tk.Label(filter_frame, text="Температура > (°C):").grid(row=0, column=3, padx=5)
        self.filter_temp_entry = tk.Entry(filter_frame, width=8)
        self.filter_temp_entry.grid(row=0, column=4, padx=5)

        tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=0, column=5, padx=10)

        # Таблица для записей
        columns = ("date", "temperature", "description", "precipitation")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("temperature", text="Температура (°C)")
        self.tree.heading("description", text="Описание")
        self.tree.heading("precipitation", text="Осадки")
        self.tree.column("date", width=100)
        self.tree.column("temperature", width=100)
        self.tree.column("description", width=250)
        self.tree.column("precipitation", width=80)

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Кнопки управления
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill="x", padx=10, pady=5)
        tk.Button(btn_frame, text="Сохранить в JSON", command=self.save_data, bg="lightblue").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Загрузить из JSON", command=self.load_data, bg="lightyellow").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Удалить выбранное", command=self.delete_selected, bg="salmon").pack(side="left", padx=5)

        self.refresh_table()

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_record(self):
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        desc = self.desc_entry.get()
      
.strip()
        precip = self.precip_var.get()

        if not date or not temp or not desc:
            messagebox.showerror("Ошибка", "Заполните все поля (дата, температура, описание)")
            return

        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        try:
            temp_val = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        self.records.append({
            "date": date,
            "temperature": temp_val,
            "description": desc,
            "precipitation": "Да" if precip else "Нет"
        })

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

        self.save_data()
        self.refresh_table()

    def apply_filters(self):
        self.refresh_table()

    def reset_filters(self):
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.refresh_table()

    def get_filtered_records(self):
        filter_date = self.filter_date_entry.get().strip()
        filter_temp_str = self.filter_temp_entry.get().strip()

        filtered = self.records[:]

        if filter_date:
            filtered = [r for r in filtered if r["date"] == filter_date]

        if filter_temp_str:
            try:
                temp_threshold = float(filter_temp_str)
                filtered = [r for r in filtered if r["temperature"] > temp_threshold]
            except ValueError:
                pass  # игнорируем некорректный ввод

        return filtered

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for rec in self.get_filtered_records():
            self.tree.insert("", tk.END, values=(
                rec["date"],
                rec["temperature"],
                rec["description"],
                rec["precipitation"]
            ))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            # Получаем значения из таблицы
            item = self.tree.item(selected[0])
            values = item["values"]
            # Ищем и удаляем запись в records
            for rec in self.records:
                if (rec["date"] == values[0] and
                    rec["temperature"] == values[1] and
                    rec["description"] == values[2] and
                    rec["precipitation"] == values[3]):
                    self.records.remove(rec)
                    break
            self.save_data()
            self.refresh_table()

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.records = json.load(f)
                self.refresh_table()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
        else:
            self.records = []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
