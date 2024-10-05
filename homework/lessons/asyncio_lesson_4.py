import asyncio
import random


async def worker_with_timeout(worker_id, queue, lock, timeout=5):
    while True:
        task = await queue.get()
        if task is None:
            print(f"Worker {worker_id} exiting...")
            queue.task_done()
            break

        try:
            async with lock:
                print(f"Worker {worker_id} is processing task {task}")

            # Задача может быть ограничена по времени с помощью wait_for
            await asyncio.wait_for(asyncio.sleep(random.uniform(0.5, 10)), timeout=timeout)
        except asyncio.TimeoutError:
            print(f"Worker {worker_id} timed out while processing {task}")

        queue.task_done()


async def main():
    # Создание очереди задач
    task_queue = asyncio.Queue()

    # Примитив блокировки для синхронизации
    lock = asyncio.Lock()

    # Запуск нескольких воркеров для обработки задач
    num_workers = 3
    workers = [asyncio.create_task(worker_with_timeout(worker_id, task_queue, lock, random.randint(1, 5))) for worker_id
               in range(1, num_workers + 1)]

    # Добавление задач в очередь
    for i in range(10):
        await task_queue.put(f"Task-{i + 1}")

    # Завершение работы воркеров
    for _ in range(num_workers):
        await task_queue.put(None)

    # Ожидание завершения всех задач в очереди
    await task_queue.join()

    # Ожидание завершения всех воркеров
    await asyncio.gather(*workers)

    print("All tasks are completed.")


# Запуск главной корутины
if __name__ == "__main__":
    asyncio.run(main())
