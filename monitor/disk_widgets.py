import tkinter as tk
from tkinter import ttk





def make_bar_disk(self):
    """Создает виджеты disk и обновляет их без моргания"""
    
    if not hasattr(self, 'disk_widgets'):
        self.disk_widgets = {}  # Храним виджеты по имени диска

    # Получение данных о дисках (информация о заполнении)
    usage_data = self.disk.disk_usage()

    # Получение информации о дисках (информация о разделах и температуре)
    disks_data = self.disk.get_disk_info()

    existing_disks = set(self.disk_widgets.keys())  # Существующие диски
    new_disks = set(partition["device"] for partition in disks_data["partitions"])  # Новые диски

    # Удаление старых виджетов, если диск больше не существует
    for disk in existing_disks - new_disks:
        for widget in self.disk_widgets[disk]:
            widget.destroy()
        del self.disk_widgets[disk]

    # Обновление или создание виджетов
    for partition in disks_data["partitions"]:
        device = partition["device"]
        fstype = partition["fstype"]
        usage = usage_data.get(device, {"percent": 0, "total": 0, "used": 0})  # Данные о заполнении
        base_device = device.split("p")[0] if "nvme" in device else device[:-1]
        temperature = disks_data["temperatures"].get(base_device, "N/A")

        # Переводим байты в гигабайты
        total_gb = round(usage['total'] / 1024**3, 2)
        used_gb = round(usage['used'] / 1024**3, 2)

        # Уникальный стиль для каждого диска
        style_name = f"Labele_Disk_{device.replace('/', '_')}"
        s2 = ttk.Style()
        s2.layout(style_name,
                  [('Labele_Disk.trough',
                   {'children': [('Labele_Disk.pbar',
                                 {'side': 'left', 'sticky': 'ns'}),
                                 ("Labele_Disk.label", {"sticky": ""})],
                    'sticky': 'nswe'})])

        if device not in self.disk_widgets:
            # Создаем новые виджеты
            disk_label = ttk.Label(self.bar_disk, text=f"{device} ({fstype}) - {temperature}°C")
            disk_pbar = ttk.Progressbar(self.bar_disk, length=250, mode='determinate', style=style_name)

            # Пакуем виджеты
            disk_label.pack(fill=tk.X, padx=2, pady=0)
            disk_pbar.pack(fill=tk.X, padx=2, pady=0)

            self.disk_widgets[device] = (disk_label, disk_pbar)



        # Обновляем значения для существующих виджетов
        if device in self.disk_widgets:
            disk_label, disk_pbar = self.disk_widgets[device]

            # Проверяем, существует ли виджет (если был удалён при переключении вкладок)
            if disk_label.winfo_exists() and disk_pbar.winfo_exists():
                disk_label['text'] = f"{device} ({fstype}) :  {temperature}°C"
                disk_pbar.configure(value=usage['percent'])

                # Уникальный текст в прогрессбаре для каждого диска
                s2.configure(style_name, text=f"{used_gb} / {total_gb} ГБ", 
                            font=("Arial", 10, "bold"), background="GREEN")
            else:
                # Если виджет не существует, удалить его из словаря
                del self.disk_widgets[device]










def make_bar_disk_1(self):
	"""Создает виджеты disk"""
	
	# Если виджет уже существует, просто обновляем значение
	if hasattr(self, 'tree') and self.tree.winfo_exists():
		self.clear_treeview()
		# Получение данных накопителей
		disks_data = self.disk.get_disk_info()

		for partition in disks_data["partitions"]:
			device = partition["device"]
			fstype = partition["fstype"]
			
			# Убираем номер раздела, чтобы найти температуру
			base_device = device.split("p")[0] if "nvme" in device else device[:-1]
			
			temperature = disks_data["temperatures"].get(base_device, "N/A")  # Берем температуру или "N/A"
			
			self.tree.insert("", "end", values=(device, fstype, temperature))
	else:

		# Создаем таблицу
		columns = ("Накопители", "Ф/С", "°C")
		self.tree = ttk.Treeview(self.bar_disk, columns=columns, show="headings")
		self.tree.heading("Накопители", text="Накопители")
		self.tree.heading("Ф/С", text="Ф/С")
		self.tree.heading("°C", text="°C")
		# self.tree.column("#0", width=0, stretch=tk.NO)  # Убираем ненужный первый столбец
		self.tree.column("Накопители", width=120)  # Задаем ширину столбца "device"
		self.tree.column("Ф/С", width=100)  # Задаем ширину столбца "fstype"
		self.tree.column("°C", width=50)  # Задаем ширину столбца "temperature"

		# Размещаем таблицу
		# self.tree.pack(expand=False, fill="both", padx=0, pady=0)
		self.tree.pack(expand=False, fill=tk.X, padx=0, pady=0)
