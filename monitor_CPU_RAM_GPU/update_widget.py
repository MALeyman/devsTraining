import tkinter as tk
from tkinter import ttk
from info_gpu import Info_gpu, global_gpu
from info_disk import InfoDisk

#from style import style2, style1

class Configure_widgets:
    def __init__(self, master, gpu, video_memory_pbar, gpu_pbar, used_video_memory_label, total_video_memory_label,
                 gpu_label, cpu, bar_one, list_label, list_pbar, ram_lab, ram_bar, gpu_temp_label, gpu_name_label, 
                 cpu_temp_label, disk_name_label, disk_temp_label, list_label_disk, tree):
        self.wheel = None
        self.master = master
        self.ram_bar = ram_bar
        self.ram_lab = ram_lab
        self.list_pbar = list_pbar
        self.list_label = list_label
        self.gpu = gpu
        self.cpu = cpu
        self.video_memory_pbar = video_memory_pbar
        self.gpu_pbar = gpu_pbar
        self.used_video_memory_label = used_video_memory_label
        self.total_video_memory_label = total_video_memory_label
        self.gpu_label = gpu_label
        self.global_gpu = global_gpu
        self.bar_one = bar_one
        self.gpu_temp_label = gpu_temp_label 
        self.gpu_name_label = gpu_name_label
        self.cpu_temp_label = cpu_temp_label 
        self.disk_temp_label = disk_temp_label
        self.tree = tree


    def update_progressbar(self):
        style2 = ttk.Style()
        # Определение стиля для прогрессбара
        style2.layout("CustomHorizontal.TProgressbar1",
                      [('CustomHorizontal.Progressbar.trough',
                        {'children': [('CustomHorizontal.Progressbar.pbar',
                                       {'side': 'left', 'sticky': 'ns'})],
                         'sticky': 'nswe'}),
                       ('CustomHorizontal.Progressbar.label', {'sticky': ''})])

        style2.configure("CustomHorizontal.TProgressbar",
                         thickness=15,
                         troughcolor='#E0E0E0',
                         bordercolor='#E0E0E0',
                         lightcolor='#E0E0E0',
                         darkcolor='#E0E0E0',
                         background='#C5E1A5',
                         troughrelief='flat')

        style1 = ttk.Style()
        # Определение стиля для прогрессбара
        style1.layout("CustomHorizontal.TProgressbar",
                      [('CustomHorizontal.Progressbar.trough',
                        {'children': [('CustomHorizontal.Progressbar.pbar',
                                       {'side': 'left', 'sticky': 'ns'})],
                         'sticky': 'nswe'}),
                       ('CustomHorizontal.Progressbar.label', {'sticky': ''})])

        style1.configure("CustomHorizontal.TProgressbar",
                         thickness=15,
                         troughcolor='#E0E0E0',
                         bordercolor='#E0E0E0',
                         lightcolor='#E0E0E0',
                         darkcolor='#E0E0E0',
                         background='#C5E1A5',
                         troughrelief='flat')

        style3 = ttk.Style()
        style3.layout("LabeledProgressbarRam",
                      [('LabeledProgressbarRam.trough',
                        {'children': [('LabeledProgressbarRam.pbar',
                                       {'side': 'left', 'sticky': 'ns'}),
                                      ("LabeledProgressbarRam.label",  #
                                       {"sticky": ""})],
                         'sticky': 'nswe'})])

        handle = self.gpu.get_handle(0)
        memory_info = self.gpu.gpu_video_memory_info(handle)
        total_memory = memory_info.total
        used_memory = memory_info.used
        memory_percentage = int((used_memory / total_memory) * 100)

        self.master.gpu_pbar["value"] = self.gpu.gpu_utilization(handle).gpu

        self.global_gpu = self.gpu.gpu_utilization(handle).gpu
        style1.configure("CustomHorizontal.TProgressbar", text=f"{memory_percentage}%", font=("Arial", 10, "bold"), background="BLUE")
        style2.configure("CustomHorizontal.TProgressbar1", text=f"{self.global_gpu}%", font=("Arial", 10, "bold"), background="GREEN")

        self.master.video_memory_pbar["value"] = memory_percentage

        self.master.gpu_label.configure(text=f"Загрузка GPU: {self.gpu.gpu_utilization(handle).gpu:.2f} %")

        self.master.total_video_memory_label.configure(text=f"Всего видеопамяти: {total_memory / (1024 * 1024):.2f} Mb")
        self.master.used_video_memory_label.configure(text=f"Занято видеопамяти: {used_memory / (1024 * 1024):.2f} Mb")

        r = self.cpu.cpu_percent_return()
        for i in range(self.cpu.cpu_count_logical):
            self.list_label[i].configure(text=f'поток {i + 1} - загрузка: {r[i]}%')
            self.list_pbar[i].configure(value=r[i])

        r2 = self.cpu.ram_usage()
        self.master.ram_lab.configure(text=f'RAM всего: {round(r2[0] / 1048576)} Мб,\
        \nИспользуется: {r2[2]}% ({round(r2[3] / 1048576)} Мб),\
        \nСвободно: {round(r2[1] / 1048576)} Мб')

        style3.configure("LabeledProgressbarRam", text=f"{r2[2]}%", background="navy")
        self.master.ram_bar.configure(value=r2[2])

        gpu_temps = self.gpu.gpu_temperatures_info()
        # Формируем строку с температурами
        if gpu_temps:
            temp_text = " | ".join([f"{name}: {temp}°C" for name, temp in gpu_temps.items()])

        else:
            temp_text = "Температура GPU недоступна"
        # Обновляем метку температуры GPU
        self.gpu_temp_label.config(text=f'{temp_text}')


   
        self.master.wheel = self.master.after(1000, self.update_progressbar)


    def update_progressbar_4(self):
        """Обновление виджетов загрузки процессора и
             оперативной памяти в 4 окне."""

        s1 = s = ttk.Style()

        ##############
        # добавим стиль прогресс бара для отображения надписи
        s.layout("Label_CPU",
                 [('Label_CPU.trough',
                   {'children': [('Label_CPU.pbar',
                                  {'side': 'left', 'sticky': 'ns'}),
                                 ("Label_CPU.label",
                                  {"sticky": ""})],
                    'sticky': 'nswe'})])
        ###################
        s1.layout("Labele_Ram",
                  [('Labele_Ram.trough',
                    {'children': [('Labele_Ram.pbar',
                                   {'side': 'left', 'sticky': 'ns'}),
                                  ("Labele_Ram.label",  #
                                   {"sticky": ""})],
                     'sticky': 'nswe'})])
        ####################
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
                     troughrelief='flat')


        r3 = self.cpu.cpu_one_return()
        self.bar_one.configure(value=r3)




        s.configure("Label_CPU", text=f"CPU:  {r3}% ",font=("Arial", 10, "bold"), background="GREEN")

        r4 = self.cpu.ram_usage()[2]
        self.ram_bar.configure(value=r4)
        s1.configure("Labele_Ram", text=f"RAM:   {r4}% ",font=("Arial", 10, "bold"), background="BLUE")




        handle = self.gpu.get_handle(0)
        memory_info = self.gpu.gpu_video_memory_info(handle)

        total_memory = memory_info.total
        used_memory = memory_info.used
        memory_percentage = int((used_memory / total_memory) * 100)

        gpu_usage = self.gpu.gpu_utilization(handle).gpu



        gpu_temps = self.gpu.gpu_temperatures_info()
        # Формируем строку с температурами
        if gpu_temps:
            temp_gpu = " | ".join([f"{name}: {temp}°C" for name, temp in gpu_temps.items()])
        else:
            temp_gpu = "Температура GPU недоступна"
        # Обновляем метку температуры GPU
        self.gpu_temp_label.config(text=f'{temp_gpu}')








        temp_cpu = self.cpu.cpu_temperature_info()
        self.cpu_temp_label.config(text=f'Температура CPU: {temp_cpu}') 





        disk_info = InfoDisk()

        # Получение данных накопителей
        disks_data = disk_info.get_disk_info()
  
       
        # for partition in disk_info["partitions"]:
        #   device = partition["device"]
        #   fstype = partition["fstype"]
          
        #   # Убираем номер раздела, чтобы найти температуру
        #   base_device = device.split("p")[0] if "nvme" in device else device[:-1]
          
        #   temperature = disk_info["temperatures"].get(base_device, "N/A")  # Берем температуру или "N/A"
          
        #   tree.insert("", "end", values=(device, fstype, temperature))
        # Заполняем таблицу данными
        self.clear_treeview()
        for partition in disks_data["partitions"]:
            device = partition["device"]
            fstype = partition["fstype"]
            
            # Убираем номер раздела, чтобы найти температуру
            base_device = device.split("p")[0] if "nvme" in device else device[:-1]
            
            temperature = disks_data["temperatures"].get(base_device, "N/A")  # Берем температуру или "N/A"
            
            self.tree.insert("", "end", values=(device, fstype, temperature))











        # self.disk_temp_label.config(text=f'{disks_data}') 
        






        self.master.gpu_pbar["value"] = self.gpu.gpu_utilization(handle).gpu
        self.global_gpu = self.gpu.gpu_utilization(handle).gpu
        s4.configure("Label_Ram_GPU", text=f"Память GPU:  {memory_percentage}%", font=("Arial", 10, "bold"), background="BLUE")
        s3.configure("Label_GPU", text=f"GPU:  {self.global_gpu}%", font=("Arial", 10, "bold"), background="GREEN")
        self.master.video_memory_pbar["value"] = memory_percentage


        self.master.wheel = self.master.after(1000, self.update_progressbar_4)






    def update_minimal_progressbar(self):
        """Обновление виджетов загрузки процессора и
             оперативной памяти в минимальном окне."""

        s1 = s = ttk.Style()

        ##############
        # добавим стиль прогресс бара для отображения надписи
        s.layout("Label_CPU",
                 [('Label_CPU.trough',
                   {'children': [('Label_CPU.pbar',
                                  {'side': 'left', 'sticky': 'ns'}),
                                 ("Label_CPU.label",
                                  {"sticky": ""})],
                    'sticky': 'nswe'})])
        ###################
        s1.layout("Labele_Ram",
                  [('Labele_Ram.trough',
                    {'children': [('Labele_Ram.pbar',
                                   {'side': 'left', 'sticky': 'ns'}),
                                  ("Labele_Ram.label",  #
                                   {"sticky": ""})],
                     'sticky': 'nswe'})])
        ####################
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
                     troughrelief='flat')


        r3 = self.cpu.cpu_one_return()
        self.bar_one.configure(value=r3)


        s.configure("Label_CPU", text=f"CPU:  {r3}% ",font=("Arial", 10, "bold"), background="GREEN")

        r4 = self.cpu.ram_usage()[2]
        self.ram_bar.configure(value=r4)
        s1.configure("Labele_Ram", text=f"RAM:   {r4}% ",font=("Arial", 10, "bold"), background="BLUE")


        handle = self.gpu.get_handle(0)
        memory_info = self.gpu.gpu_video_memory_info(handle)

        total_memory = memory_info.total
        used_memory = memory_info.used
        memory_percentage = int((used_memory / total_memory) * 100)

        gpu_usage = self.gpu.gpu_utilization(handle).gpu

        self.master.gpu_pbar["value"] = self.gpu.gpu_utilization(handle).gpu
        self.global_gpu = self.gpu.gpu_utilization(handle).gpu
        s4.configure("Label_Ram_GPU", text=f"Память GPU:  {memory_percentage}%", font=("Arial", 10, "bold"), background="BLUE")
        s3.configure("Label_GPU", text=f"GPU:  {self.global_gpu}%", font=("Arial", 10, "bold"), background="GREEN")
        self.master.video_memory_pbar["value"] = memory_percentage


        self.master.wheel = self.master.after(1000, self.update_minimal_progressbar)







    def clear_win(self):
        """Удаление виджетов."""
        for i in self.winfo_children():
            i.destroy()

    def clear_treeview(self):
        """Удаляет все строки из таблицы Treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)
