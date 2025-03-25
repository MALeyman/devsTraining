import pynvml
from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetMemoryInfo, NVMLError_LibraryNotFound
import GPUtil

global_gpu = 0.0

class Info_gpu:
    def __init__(self):
        try:
            nvmlInit()
            self.handle = nvmlDeviceGetHandleByIndex(0)  # Assuming one GPU is present
            self.device_count = nvmlDeviceGetCount()
        except NVMLError_LibraryNotFound:
            print("Библиотека pynvml не найдена. Проверьте установку и наличие видеокарты NVIDIA.")
            # Дополнительные действия, если библиотека pynvml не найдена или отсутствует видеокарта
            self.handle = None
            self.device_count = 0
        try:
            self.gpus = GPUtil.getGPUs()
            if not self.gpus:
                print("Видеокарта не найдена!")
        except Exception:
            print("Ошибка при получении информации о GPU")




    def __del__(self):
        if self.device_count > 0:
            pynvml.nvmlShutdown()

    def get_handle(self, i):
        if self.device_count > 0:
            handle = nvmlDeviceGetHandleByIndex(i)
            return handle
        else:
            return 0

    def gpu_utilization(self, handle):
        if self.device_count > 0:
            utilization = nvmlDeviceGetUtilizationRates(handle)
            return utilization
        else:
            return 0

    def gpu_video_memory_info(self, handle):
        if self.device_count > 0:
            mem_info = nvmlDeviceGetMemoryInfo(handle)
            return mem_info
        else:
            return 0

    def gpu_temperatures_info(self):
        """Получает температуру всех GPU"""
        try:
            gpus = GPUtil.getGPUs()
            gpu_temps = {}

            for gpu in gpus:
                gpu_temps[gpu.name] = gpu.temperature

            return gpu_temps  # Словарь {имя_видеокарты: температура}
        
        except Exception as e:
            print(f"Ошибка получения температуры GPU: {e}")
            return {}