import tkinter as tk
from tkinter import ttk
from info_gpu import InfoGpu, global_gpu
from gpu_widgets import make_bar_gpu
from cpu_widgets import make_bar_cpu
from ram_widgets import make_bar_ram
from disk_widgets import make_bar_disk

class Configure_widgets:
	def __init__(self, master, arguments):
		self.wheel = None
		self.master = master
		self.bar_cpu = arguments[0]
		self.ram_lab = None
		self.list_pbar = None
		self.list_label = None
		self.gpu = None
		self.cpu = None
		self.video_memory_pbar = None
		self.gpu_pbar = arguments[1]
		self.used_video_memory_label = None
		self.total_video_memory_label = None
		self.gpu_label = None
		self.global_gpu = global_gpu
		self.bar_one = None
		self.gpu_temp_label = None 
		self.gpu_name_label = None
		self.ram_bar = None

    


	def update_progressbar_0(self):
		"""Обновление виджетов загрузки процессора и
				оперативной памяти в основном окне."""

	


		make_bar_cpu(self.master)
		make_bar_ram(self.master)
		make_bar_gpu(self.master)
		make_bar_disk(self.master)

		self.master.wheel = self.master.after(1000, self.update_progressbar_0)








	def clear_win(self):
		"""Удаление виджетов."""
		for i in self.winfo_children():
			i.destroy()



	def clear_treeview(self):
		"""Удаляет все строки из таблицы Treeview"""
		for row in self.tree.get_children():
			self.tree.delete(row)














