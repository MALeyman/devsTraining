import tkinter as tk
from tkinter import ttk



def make_bar_gpu(app):
	"""Создает виджеты GPU"""

	s4 = ttk.Style()
	# Определение стиля для прогрессбара
	s4.layout("Label_Ram_GPU",
					[('Label_Ram_GPU.trough',
					{'children': [('Label_Ram_GPU.pbar',
									{'side': 'left', 'sticky': 'ns'})],
						'sticky': 'nswe'}),
					('Label_Ram_GPU.label', {'sticky': ''})])

	s4.configure("Label_Ram_GPU",
					thickness=15,
					troughcolor='#E0E0E0',
					bordercolor='#E0E0E0',
					lightcolor='#E0E0E0',
					darkcolor='#E0E0E0',
					background='#C5E1A5',
					troughrelief='flat')

	s3 = ttk.Style()
	# Определение стиля для прогрессбара
	s3.layout("Label_GPU",
					[('Label_GPU.trough',
					{'children': [('Label_GPU.pbar',
									{'side': 'left', 'sticky': 'ns'})],
						'sticky': 'nswe'}),
					('Label_GPU.label', {'sticky': ''})])

	s3.configure("Label_GPU",
					thickness=15,
					troughcolor='#E0E0E0',
					bordercolor='#E0E0E0',
					lightcolor='#E0E0E0',
					darkcolor='#E0E0E0',
					background='#C5E1A5',
					troughrelief='flat',
					orient='horizontal') 






	# Если виджет уже существует, просто обновляем значение
	if hasattr(app, 'gpu_temp_label') and app.gpu_temp_label.winfo_exists():
		
		handle = app.gpu.get_handle(0)
		memory_info = app.gpu.gpu_video_memory_info(handle)

		total_memory = memory_info.total
		used_memory = memory_info.used
		memory_percentage = int((used_memory / total_memory) * 100)

		gpu_usage = app.gpu.gpu_utilization(handle).gpu



		gpu_temps = app.gpu.gpu_temperatures_info()
		# Формируем строку с температурами
		if gpu_temps:
			temp_gpu = " | ".join([f"{name}: {temp}°C" for name, temp in gpu_temps.items()])
		else:
			temp_gpu = "Температура GPU недоступна"

		# Обновляем метку температуры GPU
		app.gpu_temp_label.config(text=f'{temp_gpu}')


		app.gpu_pbar["value"] = app.gpu.gpu_utilization(handle).gpu
		global_gpu = app.gpu.gpu_utilization(handle).gpu

		# Обновление стиля с текущими данными
		s3.configure("Label_GPU", text=f"GPU: {global_gpu}%", font=("Arial", 10, "bold"), background="GREEN")
		s4.configure("Label_Ram_GPU", text=f"Память GPU: {memory_percentage}%", font=("Arial", 10, "bold"), background="BLUE")
		app.video_memory_pbar["value"] = memory_percentage
	else:

		app.gpu_name_label = ttk.Label(app.bar_gpu, text="Температура GPU: ", anchor=tk.W, padding=(5, 0, 0, 0))
		app.gpu_name_label.pack(fill=tk.X, padx=2, pady=0)

		app.gpu_temp_label = ttk.Label(app.bar_gpu, text='', anchor=tk.W, padding=(5, 0, 0, 0))
		app.gpu_temp_label.pack(fill=tk.X, padx=2, pady=0)			
		app.gpu_pbar = ttk.Progressbar(app.bar_gpu, length=250, mode='determinate', style="Label_GPU")
		app.gpu_pbar.pack(fill=tk.X, expand=1, padx=2, pady=5)
		app.video_memory_pbar = ttk.Progressbar(app.bar_gpu, length=250, mode='determinate', style="Label_Ram_GPU")
		app.video_memory_pbar.pack(fill=tk.X, padx=2, pady=5)


















