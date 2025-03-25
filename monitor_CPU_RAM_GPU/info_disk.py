import psutil
import platform
import subprocess
import GPUtil
import cpuinfo
import re

class InfoDisk:
    """Класс для получения информации о дисках, их использовании и температуре."""

    def __init__(self):
        """Инициализация класса: получение списка реальных дисков."""
        self.disks = self.get_disks()

    def get_disks(self):
        """Получает список реальных дисков (без loop-устройств)."""
        return [disk.device for disk in psutil.disk_partitions() if "loop" not in disk.device]

    def disk_usage(self):
        """Получает использование дисков."""
        usage_info = {}
        for disk in self.disks:
            try:
                usage = psutil.disk_usage(disk)
                usage_info[disk] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
            except Exception as e:
                usage_info[disk] = {"error": str(e)}
        return usage_info







    def get_disk_info(self):
        disk_info = {}
        # Получение информации о разделах
        disk_info["partitions"] = [
            {"device": disk.device, "fstype": disk.fstype}
            for disk in psutil.disk_partitions() if not disk.device.startswith('/dev/loop')
        ]

        # Получение температуры дисков
        temperature_info = {}
        try:
            # Получаем список всех физических дисков, исключая loop-устройства
            output = subprocess.check_output("lsblk -nd -o NAME", shell=True).decode().split()
            disk_list = [f"/dev/{disk}" for disk in output if not disk.startswith("loop")]

            for disk in disk_list:
                try:
                    if "nvme" in disk:
                        # Проверка NVMe диска с полным путем
                        temp_output = subprocess.check_output(f"sudo nvme smart-log {disk} | grep Temperature", shell=True).decode()
                        match = re.search(r"Temperature Sensor 1\s*:\s*(\d+)\s*°C", temp_output)
                        temperature = int(match.group(1)) 
                        # print("Температура:", temperature)
                    elif "sdb" in disk:
                        temp_output = subprocess.check_output(f"sudo smartctl -A {disk} | grep Temperature", shell=True).decode()
                        # print("Температура:")
                        parts = temp_output.split()  
                        # print(parts)
                        temperature = int(parts[-1]) 
                        # print("Температура:", temperature)
                    else:
                        # Проверка SATA/SSD/HDD с полным путем
                        temp_output = subprocess.check_output(f"sudo smartctl -A {disk} | grep Temperature", shell=True).decode()
                        match = re.search(r"(\d+)\s+\(Min/Max", temp_output)
                        temperature = int(match.group(1)) 
                        # print("Температура:", temperature)
                    # print(disk)
                    # print(type(temp_output))
                    # print(temp_output)
                    temperature_info[disk] = temperature
                    # print(f"{disk}: {temp_output.strip()}")
                except subprocess.CalledProcessError:
                    print(f"{disk}: Температура недоступна (возможно, диск не поддерживает SMART)")
        except Exception as e:
            print(f"Ошибка получения списка дисков: {e}")
        disk_info["temperatures"] = temperature_info
        return disk_info



if __name__ == "__main__":

    output = subprocess.check_output("lsblk -nd -o NAME", shell=True).decode().split()
    disk_list = [f"/dev/{disk}" for disk in output if not disk.startswith("loop")]
    print(disk_list)
    # Использование класса
    disk_info = InfoDisk()

    # Получение данных
    disks_data = disk_info.get_disk_info()
    usage_data = disk_info.disk_usage()
    # print(disks_data['temperatures'])
    

    # Пример использования (без print)
    # Можно передавать данные в логи, API или другую систему
    data = {
        "disks": disks_data,
        "usage": usage_data,
    }
    # print(data)