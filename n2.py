from multiprocessing import Process, Lock
import time
from random import choice
from string import ascii_lowercase
import os
import random


#https://stackoverflow.com/questions/28619542/generate-a-random-string-with-a-random-number-of-letters-and-spaces
chars = ascii_lowercase + " " * 10
main_file = 'output.txt'


#Возвращает случайную строку длиной n символов
def random_string(n):
    return "".join(choice(chars) for _ in range(n))


#Записываем слово в файл — Lock не даёт двум процессам писать одновременно
def write_word(lock, word, filename):
    with lock:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(word + "\n")
        
        
def multi_processing(words,filename):
    start = time.time()
    lock = Lock()
    processes = []

    for word in words:
        proc = Process(target=write_word, args=(lock, word, filename))
        proc.start()
        processes.append(proc)

    for proc in processes:
        proc.join()

    mp_time = time.time() - start
    print('Многопроцессорное вычисление: ', mp_time, 'сек')
    
def run_mp_test():

    #Удаляем старый файл, если он есть
    if os.path.exists(main_file):
        os.remove(main_file)
        
    #Генерируем строки
    words = []
    for i in range(10):                
        text = random_string(random.randint(40, 70))
        words.append(f"Процесс {i+1}: {text}")

    multi_processing(words, main_file)
    
    if os.path.exists(main_file):
        with open(main_file, "r", encoding="utf-8") as f:
            print(f.read())
            
if __name__ == "__main__":
    run_mp_test()
