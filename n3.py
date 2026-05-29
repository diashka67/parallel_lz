import asyncio
import time
import random

#Производитель
async def prod(queue, producer_id):
    for i in range(1, 6):
        await queue.put(i)
        print('создал', i)
        await asyncio.sleep(random.uniform(0.1, 0.5))
    



#Потребитель
async def cons(queue):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"Потребитель обработал {item}")
        queue.task_done()


async def asyncio_def():
    start = time.time()
    queue = asyncio.Queue(maxsize=10)
    
    #создаём 3 производителя
    producers = [asyncio.create_task(prod(queue, i)) for i in range(3)]
    
    #создаём 1 потребителя
    consumer_task = asyncio.create_task(cons(queue))
    
    #ждем пока производители закончат
    await asyncio.gather(*producers)
    
    #ждем пока потребитель обработает все элементы, попавшие в очередь
    await queue.join()
    
    await queue.put(None)
    
    #ждем корректного завершения корутины потребителя
    await consumer_task
    
    mp_time = time.time()-start
    print(f'Асинхронное выполнение: {mp_time}')

def async_queue():
    asyncio.run(asyncio_def())
    
if __name__ == "__main__":
    async_queue()