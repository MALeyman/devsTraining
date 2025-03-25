

import psutil as pt
import subprocess

class InfoCpu():
    """Использование процессора и оперативной памяти."""

    def __init__(self):
        """Количество физических и логических ядер процессора."""
        self.cpu_count = pt.cpu_count(logical=False)
        self.cpu_count_logical = pt.cpu_count()

    def cpu_percent_return(self):
        """Считывает нагрузку на ядра процессора."""
        return pt.cpu_percent(percpu=True)

    def cpu_one_return(self):
        """Считывает общую загрузку процессора."""
        return pt.cpu_percent()

    def ram_usage(self):
        """Считывает загрузку оперативной памяти."""
        return pt.virtual_memory()

    def cpu_temperatures_info(self):
        """Получает температуру процессора"""
        try:
            output = subprocess.check_output("sensors", shell=True).decode()
            for line in output.split("\n"):
                if "Core" in line or "Tdie" in line:
                    print(line.strip())
        except Exception as e:
            print(f"Ошибка получения температуры CPU: {e}")

    def cpu_temperature_info(self):
        """Получает общую температуру процессора"""
        try:
            output = subprocess.check_output("sensors", shell=True).decode()
            for line in output.split("\n"):
                if "Package id" in line or "Tctl" in line:  # Ищем общую температуру
                    # print(line.strip())  # Выводим строку с температурой
                    return float(line.split("+")[1].split("°C")[0].strip())  # Возвращаем числовое значение
        except Exception as e:
            print(f"Ошибка получения температуры CPU: {e}")
            return None