"""
    Автор: Лейман М.А.
    Дата создания: 10.04.2025
"""

"""  
    ===== Горячие клавиши: =====

    "s"         # Сохранение
    "m"         # Выбор класса
    "q"         # Выход
    "d"         # Пропустить изображение

"""



import os
import tkinter as tk
from tkinter import Canvas, filedialog
from PIL import Image, ImageTk
import cv2
import glob
from tkinter import simpledialog
import shutil
import random

# Получаем текущую рабочую папку  
current_directory = os.getcwd()  

# /home/maksim/develops/python/dataset/dataset_DOTA/dataset_DOTA/images_jpeg/
# /home/maksim/develops/python/devsTraining/zala_task/dataset/dataset_DOTA/dataset_DOTA/images_jpeg/

path_dataset = os.path.join(current_directory, "devsTraining/zala_task/dataset")

image_2 = 'dataset_DOTA/dataset_DOTA/images_jpeg/'   
images_path_1 = os.path.join(path_dataset, image_2) 

labels_2 = 'dataset_DOTA/dataset_DOTA/cleaned_labels/'   
labels_path = os.path.join(path_dataset, labels_2)  

print(images_path_1)

#  Папки 
images_path = images_path_1
labels_path = labels_path
output_images_dir = "output_images"
output_labels_dir = "output_labels"
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_labels_dir, exist_ok=True)

#  Переменные 
image_files = sorted(glob.glob(os.path.join(images_path, "*.jpg")))
current_index = 0
boxes = []
new_boxes = []
drawing = False
start_x = start_y = 0
current_rect = None
current_class_id = 0
img = None
tk_img = None

#  Окно
root = tk.Tk()
root.title("YOLO Аннотации")

# canvas = Canvas(root, cursor="cross")
# canvas.pack(fill=tk.BOTH, expand=True)

# #  Скроллинг 
# x_scroll = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=canvas.xview)
# y_scroll = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
# canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
# x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
# y_scroll.pack(side=tk.RIGHT, fill=tk.Y)


frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = Canvas(frame, cursor="cross", bg="black")
canvas.grid(row=0, column=0, sticky="nsew")

x_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
x_scroll.grid(row=1, column=0, sticky="ew")

y_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
y_scroll.grid(row=0, column=1, sticky="ns")

frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

canvas.configure(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)


def load_image(index):
    global img, tk_img, boxes, new_boxes
    if index >= len(image_files):
        print("Все изображения размечены.")
        root.quit()
        return

    img_path = image_files[index]
    print(f"\nЗагрузка: {img_path}")
    filename = os.path.basename(img_path)
    root.title(f"YOLO Аннотации — {filename}")

    cv_img = cv2.imread(img_path)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv_img)
    tk_img = ImageTk.PhotoImage(img)

    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=tk_img)
    canvas.config(scrollregion=canvas.bbox(tk.ALL))

    boxes.clear()
    new_boxes.clear()

    # Загрузка YOLO разметки
    basename = os.path.splitext(os.path.basename(img_path))[0]
    label_file = os.path.join(labels_path, f"{basename}.txt")
    if os.path.exists(label_file):
        with open(label_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                cls, x, y, w, h = map(float, parts)
                w_img, h_img = img.size
                x1 = int((x - w / 2) * w_img)
                y1 = int((y - h / 2) * h_img)
                x2 = int((x + w / 2) * w_img)
                y2 = int((y + h / 2) * h_img)
                boxes.append((int(cls), x1, y1, x2, y2))
    redraw()

# def redraw():
#     canvas.delete("box")
#     for cls, x1, y1, x2, y2 in boxes:
#         canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=2, tags="box")
#         canvas.create_text(x1 + 4, y1 - 10, text=str(cls), anchor="nw",
#                    fill="green", font=("Arial", 14, "bold"), tags="box")



def redraw():
    canvas.delete("box")

    # === Нарисовать сетку ===
    grid_spacing = 100  # Размер клетки сетки в пикселях
    w_img, h_img = img.size

    for x in range(0, w_img, grid_spacing):
        canvas.create_line(x, 0, x, h_img, fill="gray", dash=(2, 4), tags="box")
    for y in range(0, h_img, grid_spacing):
        canvas.create_line(0, y, w_img, y, fill="gray", dash=(2, 4), tags="box")

    # === Нарисовать все текущие боксы ===
    for cls, x1, y1, x2, y2 in boxes:
        canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=2, tags="box")
        canvas.create_text(x1 + 4, y1 - 10, text=str(cls), anchor="nw",
                           fill="green", font=("Arial", 14, "bold"), tags="box")




def on_mouse_down(event):
    global drawing, start_x, start_y, current_rect
    drawing = True
    start_x = canvas.canvasx(event.x)
    start_y = canvas.canvasy(event.y)
    current_rect = canvas.create_rectangle(start_x, start_y, start_x, start_y,
                                           outline="blue", width=1, tags="box")

def on_mouse_move(event):
    if not drawing or current_rect is None:
        return
    cur_x = canvas.canvasx(event.x)
    cur_y = canvas.canvasy(event.y)
    canvas.coords(current_rect, start_x, start_y, cur_x, cur_y)

def on_mouse_up(event):
    global drawing, current_rect
    if not drawing or current_rect is None:
        return
    drawing = False
    end_x = canvas.canvasx(event.x)
    end_y = canvas.canvasy(event.y)
    x1, y1 = int(min(start_x, end_x)), int(min(start_y, end_y))
    x2, y2 = int(max(start_x, end_x)), int(max(start_y, end_y))
    boxes.append((current_class_id, x1, y1, x2, y2))
    new_boxes.append((current_class_id, x1, y1, x2, y2))
    redraw()
    current_rect = None

def on_right_click(event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    for i in range(len(boxes) - 1, -1, -1):
        cls, x1, y1, x2, y2 = boxes[i]
        if x1 <= x <= x2 and y1 <= y <= y2:
            boxes.pop(i)
            redraw()
            break

def yolo_format(x1, y1, x2, y2, cls):
    w_img, h_img = img.size
    x_center = ((x1 + x2) / 2) / w_img
    y_center = ((y1 + y2) / 2) / h_img
    w = abs(x2 - x1) / w_img
    h = abs(y2 - y1) / h_img
    return f"{cls} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}"

def save_and_next():
    global current_index
    if img:
        img_file = os.path.basename(image_files[current_index])
        img.save(os.path.join(output_images_dir, img_file))

        label_file = os.path.splitext(img_file)[0] + ".txt"
        with open(os.path.join(output_labels_dir, label_file), "w") as f:
            for cls, x1, y1, x2, y2 in boxes:
                f.write(yolo_format(x1, y1, x2, y2, cls) + "\n")
        print(f"Сохранено: {img_file}")

    current_index += 1
    load_image(current_index)


def change_class_id():
    global current_class_id
    new_id = simpledialog.askstring("Выбор класса", "Введите новый class_id:")
    if new_id is not None:
        try:
            current_class_id = int(new_id)
            print(f"Теперь размечаем класс: {current_class_id}")
        except ValueError:
            print("Некорректный ввод.")




def skip_image():
    global current_index
    current_index += 1
    load_image(current_index)

# === Привязка событий ===
canvas.bind("<Button-1>", on_mouse_down)
canvas.bind("<B1-Motion>", on_mouse_move)
canvas.bind("<ButtonRelease-1>", on_mouse_up)
canvas.bind("<Button-3>", on_right_click)

root.bind("s", lambda e: save_and_next())   # Сохранение
root.bind("m", lambda e: change_class_id()) # Выбор класса
root.bind("q", lambda e: root.quit())       # Выход
root.bind("d", lambda e: skip_image())      # Пропустить изображение

load_image(current_index)
root.mainloop()


