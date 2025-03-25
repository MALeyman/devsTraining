import tkinter as tk
from tkinter import ttk



def make_bar_ram(self):
	"""Создает виджеты RAM"""

	s1 = ttk.Style()

	s1.layout("Labele_Ram",
				[('Labele_Ram.trough',
				{'children': [('Labele_Ram.pbar',
								{'side': 'left', 'sticky': 'ns'}),
								("Labele_Ram.label",  #
								{"sticky": ""})],
					'sticky': 'nswe'})])


	
	
	# Если виджет уже существует, просто обновляем значение
	if hasattr(self, 'ram_bar') and self.ram_bar.winfo_exists():
		r4 = self.cpu.ram_usage()[2]
		self.ram_bar.configure(value=r4)
		s1.configure("Labele_Ram", text=f"RAM:   {r4}% ",font=("Arial", 10, "bold"), background="BLUE") 
		
	else:
		# Создание нового виджета, если его ещё нет
		self.ram_bar = ttk.Progressbar(self.bar_ram, length=250,mode='determinate', style="Labele_Ram")
		self.ram_bar.pack(fill=tk.X, side=tk.LEFT, expand=1, padx=2, pady=5)


