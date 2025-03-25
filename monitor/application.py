import tkinter as tk
from tkinter import ttk, BOTH
import sys
from info_cpu import InfoCpu

from info_gpu import InfoGpu, global_gpu
from info_disk import InfoDisk
from update_widget import Configure_widgets
from gpu_widgets import make_bar_gpu
from cpu_widgets import make_bar_cpu
from ram_widgets import make_bar_ram
from disk_widgets import make_bar_disk


"""Создает графический интерфейс."""
class Application(tk.Tk, Configure_widgets):
    """Создаёт окно."""
    def __init__(self):
        tk.Tk.__init__(self)
        self.iconphoto(True, tk.PhotoImage(file='/home/maksim/myapp/monitor_CPU_RAM_GPU/icon.png'))

        self.title('Мониторинг')
        self.attributes('-alpha', 0.9)
        self.attributes('-topmost', False)
        self.overrideredirect(False)
        self.resizable(True, True)
        self.geometry("250x1000")
        self.minsize(200, 100)
        self.maxsize(600, 1200)

        self.make_vidgets()

        self.run_main_ui()






    # вкладка информации о программе
    def make_info_win(self):
        '''Вкладка информация о программе'''
        info_win = tk.Toplevel(self)
        info_win.title("О программе")
        info_win.geometry("330x150")
        info_win.resizable(False, False)
        info_win.bar = ttk.Frame(info_win)
        info_win.bar.pack(fill=tk.X)
        ttk.Button(info_win.bar, text='<< Назад', command=info_win.destroy).pack(side=tk.LEFT)
        info_win.bar2 = ttk.LabelFrame(info_win, text='   Программа мониторинг ресурсов')
        info_win.bar2.pack(fill=tk.X)
        info_win.lab1 = ttk.Label(info_win.bar2, text='     \
                                \n   Программа реализована на Python 3, с применением \
                                \n   библиотек tkinter, psutill и pynvml.\
                                \n \
                                \n              Накодил  Лейман М.А.\
                                \n              почта: makc.mon@mail.ru \
                                \n                     ').pack(fill=tk.X, side=tk.LEFT)


        info_win.update()
        info_win.grab_set()

        if self.wheel is not None:
            self.after_cancel(self.wheel)
            self.wheel = None
        info_win.protocol("WM_DELETE_WINDOW", info_win.destroy)

    # Список выбора отображения окна
    def choise_combo(self, event):
        """
        Выбранное событие в выпадающем списке.
        Прерывание цикла обновления виджетов.
        Развязывание событий, удаление виджетов.
        Создание виджетов небольших окон.
        """
        if self.combo_win.current() == 1:
            self.combo_win.unbind('<<ComboboxSelected>>')
            if self.wheel is not None:
                self.after_cancel(self.wheel)
                self.wheel = None
            self.clear_win()
            self.update()
            self.make_vidgets()
            self.run_main_ui() # минимальное окно
        elif self.combo_win.current() == 0:
            self.combo_win.unbind('<<ComboboxSelected>>')
            if self.wheel is not None:
                self.after_cancel(self.wheel)
                self.wheel = None
            self.clear_win()
            self.update()
            self.make_vidgets()
            self.run_main_ui() # Возврат к основному окну
        elif self.combo_win.current() == 2:
            self.combo_win.unbind('<<ComboboxSelected>>')
            if self.wheel is not None:
                self.after_cancel(self.wheel)
                self.wheel = None
            self.clear_win()
            self.update()
            self.make_vidgets()
            self.run_main_ui() # Окно CPU
        elif self.combo_win.current() == 3:
            self.combo_win.unbind('<<ComboboxSelected>>')
            if self.wheel is not None:
                self.after_cancel(self.wheel)
                self.wheel = None
            self.clear_win()
            self.update()
            self.make_vidgets()
            self.run_main_ui() # Окно накопители           
        else:
            self.combo_win.unbind('<<ComboboxSelected>>')
            if self.wheel is not None:
                self.after_cancel(self.wheel)
                self.wheel = None
            self.clear_win()
            self.make_vidgets()
            self.update()  
            self.run_main_ui() # Окно GPU


    #  создание виджетов
    def make_vidgets(self):
        """
            Инициализация виджетов
        """
        
        self.gpu_pbar_var = tk.DoubleVar()           # Переменная для связи с прогрессбаром gpu_pbar
        self.video_memory_pbar_var = tk.DoubleVar()  # Переменная для связи с прогрессбаром video_memory_pbar
        self.cpu_pbar_var = tk.DoubleVar()
        self.ram_pbar_var = tk.DoubleVar()

        self.gpu = InfoGpu()
        self.cpu = InfoCpu()
        self.disk = InfoDisk()

        self.label1 = None
        self.combo_win = None
        self.bar_gpu = None         # bar1
        self.bar_head = None        # bar2
        self.bar_cpu = None         # bar3
        self.bar_ram = None         # bar4
        self.bar_disk = None        # bar5

        # self.ram_bar = None
        self.gpu_pbar = None
        self.wheel = None
        self.bar_one = None
        # self.tree = None

        self.arguments = [self.bar_cpu, self.gpu_pbar]

        self.list_label_disk = []

        self.bar_gpu = ttk.LabelFrame(self, text='ИНДИКАТОРЫ GPU')

        self.bar_cpu = ttk.LabelFrame(self, text='ИНДИКАТОРЫ CPU')

        self.bar_ram = ttk.LabelFrame(self, text='ИНДИКАТОРЫ RAM')

        self.bar_disk = ttk.LabelFrame(self, text='ИНДИКАТОРЫ НАКОПИТЕЛЕЙ')

        self.bar_head = ttk.Frame(self)
        self.bar_head.pack(fill=tk.X)

        self.combo_win = ttk.Combobox(self.bar_head,
                                      values=["Основное", "Мин", "CPU", "Накопители", "GPU"],
                                      width=11, state='readonly')
        # self.combo_win.current(0)
        self.combo_win.pack(side=tk.LEFT)
        ttk.Button(self.bar_head, text='О программе', command=self.make_info_win).pack(side=tk.LEFT)  # вкладка информации о программе
        self.combo_win.bind('<<ComboboxSelected>>', self.choise_combo)  # Список выбора отображения окна 

        


    # 0. Основное окно
    def run_main_ui(self):
        """Создание Основного окна."""

        self.geometry("280x600")
        self.combo_win.current(0)

        self.bar_cpu.pack(fill=tk.Y)
        self.bar_ram.pack(fill=tk.Y)
        self.bar_gpu.pack(fill=tk.Y)
        self.bar_disk.pack(fill=tk.Y)
        # self.gpu_pbar = ttk.Progressbar(self.bar_gpu, length=250, mode='determinate')
        
        make_bar_cpu(self)
        make_bar_ram(self)
        make_bar_gpu(self)
        make_bar_disk(self)
        

        self.configure_widgets(0)


    def configure_widgets(self, num=0):
        """
            Конфигурация виджетов
        """
        self.configure = Configure_widgets(self, self.arguments)     
        if num == 0:
            self.configure.update_progressbar_0()        
        elif num == 1:
            self.configure.update_progressbar_0()
        elif num == 2:
            self.configure.update_progressbar_0()
        elif num == 3:
            self.configure.update_progressbar_0()               
        elif num == 4:
            self.configure.update_progressbar_0()
        else:
            self.configure.update_progressbar_0()
















