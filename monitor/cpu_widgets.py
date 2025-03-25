import tkinter as tk
from tkinter import ttk
import psutil as pt
import subprocess
	
def make_bar_cpu(self):
	"""Создает или обновляет виджеты CPU"""

	s = ttk.Style()
	s.layout("Label_CPU",
			[('Label_CPU.trough',
				{'children': [('Label_CPU.pbar',
								{'side': 'left', 'sticky': 'ns'}),
							("Label_CPU.label",
								{"sticky": ""})],
				'sticky': 'nswe'})])

	# print(self.bar_one_cpu)
	# Если виджет уже существует, просто обновляем значение
	if hasattr(self, 'bar_one_cpu') and self.bar_one_cpu.winfo_exists():
		temp_cpu = self.cpu.cpu_temperature_info()
		self.cpu_temp_label.config(text=f'Температура CPU: {temp_cpu}') 
		
	else:
		# Создание нового виджета, если его ещё нет
		self.cpu_temp_label = ttk.Label(self.bar_cpu, text='', anchor=tk.W, padding=(0, 0, 0, 0))
		self.cpu_temp_label.pack(fill=tk.X, padx=2, pady=0)

		self.bar_one_cpu = ttk.Progressbar(self.bar_cpu, length=250, mode='determinate', style="Label_CPU")
		self.bar_one_cpu.pack(fill=tk.X, side=tk.LEFT, expand=1, padx=2, pady=5)

	r3 = pt.cpu_percent()
	self.bar_one_cpu.configure(value=r3)
	s.configure("Label_CPU", text=f"CPU:  {r3}% ",font=("Arial", 10, "bold"), background="GREEN")
