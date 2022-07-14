from sys import platform
import time
import threading
import json
import psutil

print("Collecting datas")
interval_sec = input("Enter time interval between data collection iterations (sec): ")
run = True
        
def collecting_data(interval_sec):
    global run
    datas = []
    while run:
        p = psutil.Process()
        data = {
            "cpu": psutil.cpu_percent(),
            "memory consumption": {
                "resident_set_size": p.memory_info().rss,
                "virtual_memory_size": p.memory_info().vms
            },
            "file_descriptors": p.num_fds()
        }
        datas.append(data)
        time.sleep(int(interval_sec))
    write_json({"data": datas}, "data_collection.json")

def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=3)

if platform == "linux" or platform == "linux2" or platform == "darwin":
    while run:
        t = threading.Thread(target=collecting_data, args=interval_sec)
        t.start()
        if input("quit? (Y/N): ") == 'Y':
            run = False


