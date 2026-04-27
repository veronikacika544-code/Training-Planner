import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary / Дневник погоды")
        self.root.geometry("800x600")
        
        # Данные
        self.weather_records = []
        self.filename = "weather_records.json"
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка данных
        self.load_records()
        
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавить новую запись", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Дата
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, sticky="w", pady=5)
        ttk.Label(input_frame, text="Например: 26.04.2026").grid(row=0, column=2, sticky="w", pady=5)
        
        # Температура
        ttk.Label(input_frame, text="Температура (°C):").grid(row=1, column=0, sticky="w", pady=5)
        self.temp_entry = ttk.Entry(input_frame, width=20)
        self.temp_entry.grid(row=1, column=1, sticky="w", pady=5)
        
        # Описание погоды
        ttk.Label(input_frame, text="Описание погоды:").grid(row=2, column=0, sticky="w", pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)
        
        # Осадки
        ttk.Label(input_frame, text="Осадки:").grid(row=3, column=0, sticky="w", pady=5)
        self.precip_var = tk.BooleanVar()
        self.precip_check = ttk.Checkbutton(input_frame, text="Да", variable=self.precip_var)
        self.precip_check.grid(row=3, column=1, sticky="w", pady=5)
        
        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="Добавить запись", command=self.add_record)
        self.add_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Фрейм для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding="10")
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, sticky="w", pady=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=20)
        self.filter_date_entry.grid(row=0, column=1, sticky="w", pady=5)
        self.filter_date_button = ttk.Button(filter_frame, text="Применить", 
                                            command=self.filter_by_date)
        self.filter_date_button.grid(row=0, column=2, pady=5, padx=5)
        self.clear_date_filter = ttk.Button(filter_frame, text="Сбросить", 
                                           command=self.clear_date_filter)
        self.clear_date_filter.grid(row=0, column=3, pady=5, padx=5)
        
        # Фильтр по температуре
        ttk.Label(filter_frame, text="Фильтр по температуре:").grid(row=1, column=0, sticky="w", pady=5)
        self.filter_temp_entry = ttk.Entry(filter_frame, width=20)
        self.filter_temp_entry.grid(row=1, column=1, sticky="w", pady=5)
        ttk.Label(filter_frame, text="°C и выше").grid(row=1, column=2, sticky="w", pady=5)
        self.filter_temp_button = ttk.Button(filter_frame, text="Применить", 
                                            command=self.filter_by_temperature)
        self.filter_temp_button.grid(row=1, column=2, pady=5, padx=5)
        self.clear_temp_filter = ttk.Button(filter_frame, text="Сбросить", 
                                           command=self.clear_temp_filter)
        self.clear_temp_filter.grid(row=1, column=3, pady=5, padx=5)
        
        # Таблица для отображения записей
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, pad
self.date - self Ресурсы и информация.
www.self.date

x=10, pady=5)
        
        # Создание таблицы
        columns = ("date", "temperature", "description", "precipitation")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Определение заголовков
        self.tree.heading("date", text="Дата")
        self.tree.heading("temperature", text="Температура (°C)")
        self.tree.heading("description", text="Описание")
        self.tree.heading("precipitation", text="Осадки")
        
        # Определение ширины колонок
        self.tree.column("date", width=150)
        self.tree.column("temperature", width=150)
        self.tree.column("description", width=300)
        self.tree.column("precipitation", width=100)
        
        # Добавление скроллбаров
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Размещение элементов
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        
        # Кнопки управления
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        self.save_button = ttk.Button(control_frame, text="Сохранить в JSON", command=self.save_records)
        self.save_button.pack(side="left", padx=5)
        
        self.load_button = ttk.Button(control_frame, text="Загрузить из JSON", command=self.load_records)
        self.load_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(control_frame, text="Очистить все записи", command=self.clear_all_records)
        self.clear_button.pack(side="left", padx=5)
        
        self.show_all_button = ttk.Button(control_frame, text="Показать все записи", command=self.show_all_records)
        self.show_all_button.pack(side="left", padx=5)
        
    def validate_input(self, date_str, temp_str, desc_str):
        # Проверка даты
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return False
        
        # Проверка температуры
        try:
            float(temp_str.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return False
        
        # Проверка описания
        if not desc_str.strip():
            messagebox.showerror("Ошибка", "Описание погоды не может быть пустым!")
            return False
        
        return True
    
    def add_record(self):
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        desc_str = self.desc_entry.get().strip()
        precipitation = self.precip_var.get()
        
        if not self.validate_input(date_str, temp_str, desc_str):
            return
        
        try:
            temperature = float(temp_str.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
        
        record = {
            "date": date_str,
            "temperature": temperature,
            "description": desc_str,
            "precipitation": precipitation
        }
        
        self.weather_records.append(record)
        self.update_table(self.weather_records)
        
        # Очистка полей ввода
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
        
        messagebox.showinfo("Успех", "Запись добавлена успешно!")
    
    def update_table(self, records):
        # Очистка таблицы
        for item in self.tree.get_childre

n():
            self.tree.delete(item)
        
        # Заполнение таблицы
        for record in records:
            precip_text = "Да" if record["precipitation"] else "Нет"
            self.tree.insert("", "end", values=(
                record["date"],
                f"{record['temperature']:.1f}",
                record["description"],
                precip_text
            ))
    
    def filter_by_date(self):
        filter_date = self.filter_date_entry.get().strip()
        
        if not filter_date:
            messagebox.showwarning("Предупреждение", "Введите дату для фильтрации!")
            return
        
        try:
            datetime.strptime(filter_date, "%d.%m.%Y")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
            return
        
        filtered_records = [record for record in self.weather_records 
                           if record["date"] == filter_date]
        
        self.update_table(filtered_records)
        messagebox.showinfo("Информация", f"Найдено записей: {len(filtered_records)}")
    
    def clear_date_filter(self):
        self.filter_date_entry.delete(0, tk.END)
        self.update_table(self.weather_records)
    
    def filter_by_temperature(self):
        temp_str = self.filter_temp_entry.get().strip()
        
        if not temp_str:
            messagebox.showwarning("Предупреждение", "Введите температуру для фильтрации!")
            return
        
        try:
            min_temp = float(temp_str.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
        
        filtered_records = [record for record in self.weather_records 
                           if record["temperature"] >= min_temp]
        
        self.update_table(filtered_records)
        messagebox.showinfo("Информация", f"Найдено записей: {len(filtered_records)}")
    
    def clear_temp_filter(self):
        self.filter_temp_entry.delete(0, tk.END)
        self.update_table(self.weather_records)
    
    def save_records(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.weather_records, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", f"Записи сохранены в файл {self.filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def load_records(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.weather_records = json.load(f)
                self.update_table(self.weather_records)
                messagebox.showinfo("Успех", f"Записи загружены из файла {self.filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
        else:
            messagebox.showinfo("Информация", "Файл с записями не найден")
    
    def clear_all_records(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить все записи?"):
            self.weather_records = []
            self.update_table(self.weather_records)
            messagebox.showinfo("Информация", "Все записи удалены")
    
    def show_all_records(self):
        self.update_table(self.weather_records)

def main():
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()

if __name__ == "__main__":
    main()
