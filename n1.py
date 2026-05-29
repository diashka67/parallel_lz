import threading
import os
import time

#создаем папку для тестовых файлов
os.makedirs("random_txt_files", exist_ok=True)

#генерируем 50 файлов.
for i in range(1, 51):
    if i == 25:
        text = "error"
    else:
        text = "ok"
    with open(f"random_txt_files/file_{i}.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
files = os.listdir('random_txt_files')  

def find(word='error'):
    found_files = []
    for one_file in files:
        with open(f'random_txt_files/{one_file}', "r") as file:
            content = file.read()
        if word in content:
            found_files.append(one_file)
    time.sleep(1)
    return found_files


def synhron():
    start = time.time()
    find('error')
    our_time = time.time() - start
    print('Синхронное время:', our_time,'секунд')
    
    
def threads():
    start = time.time()
    threads = []
    
    
    #cоздаем 10 потоков
    for i in range(10):
        t = threading.Thread(target=find, args=('error',))
        t.start()
        threads.append(t)
        
    for t in threads:
        t.join()
        
    threads_time = time.time() - start
    print('Время с потоками:',threads_time, 'секунд')
        
if __name__ == "__main__":
    print("Запускаем тесты...\n")
    synhron()
    threads()


