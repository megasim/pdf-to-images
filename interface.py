import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pdf2image import convert_from_path


def select_pdf():
    """Выбор PDF-файла"""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, file_path)


def select_output_folder():
    """Выбор папки для сохранения"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder_path)


def convert_pdf():
    """Фоновая конвертация PDF в изображения"""

    def task():
        pdf_path = pdf_entry.get()
        output_folder = output_entry.get()

        if not pdf_path or not output_folder:
            messagebox.showwarning("Ошибка", "Выберите PDF-файл и папку для сохранения!")
            return

        try:
            os.makedirs(output_folder, exist_ok=True)
            images = convert_from_path(pdf_path, fmt="png")

            if not images:
                messagebox.showerror("Ошибка", "Не удалось обработать PDF.")
                return

            progress["maximum"] = len(images)

            for i, image in enumerate(images):
                image_path = os.path.join(output_folder, f"page_{i + 1}.png")
                image.save(image_path, "PNG")
                progress["value"] = i + 1
                root.update_idletasks()

            messagebox.showinfo("Готово!", f"Сохранено {len(images)} изображений в {output_folder}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    # Запуск конвертации в отдельном потоке
    thread = threading.Thread(target=task)
    thread.start()


# Создание окна
root = tk.Tk()
root.title("PDF в изображения")
root.geometry("500x250")
root.resizable(False, False)

# Поле выбора PDF
tk.Label(root, text="Выберите PDF-файл:").pack(pady=5)
pdf_entry = tk.Entry(root, width=50)
pdf_entry.pack(pady=2)
tk.Button(root, text="Обзор", command=select_pdf).pack(pady=2)

# Поле выбора папки
tk.Label(root, text="Выберите папку для сохранения:").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=2)
tk.Button(root, text="Обзор", command=select_output_folder).pack(pady=2)

# Кнопка конвертации
tk.Button(root, text="Конвертировать", command=convert_pdf, bg="green", fg="white").pack(pady=10)

# Полоска прогресса
progress = Progressbar(root, length=400, mode="determinate")
progress.pack(pady=5)

# Запуск GUI
root.mainloop()
