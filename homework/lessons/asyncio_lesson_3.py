import asyncio
import random

# Пример асинхронной задачи
async def worker(worker_id, queue, lock):
    while True:
        # Получение задачи из очереди
        task = await queue.get()

        # Завершение работы при получении None
        if task is None:
            print(f"Worker {worker_id} exiting...")
            queue.task_done()
            break

        # Симуляция выполнения задачи с произвольной задержкой
        async with lock:
            print(f"Worker {worker_id} is processing task {task}")
        await asyncio.sleep(random.uniform(0.5, 2))

        # Уведомляем очередь, что задача выполнена
        queue.task_done()

async def main():
    # Создание очереди задач
    task_queue = asyncio.Queue()

    # Примитив блокировки для синхронизации
    lock = asyncio.Lock()

    # Запуск нескольких воркеров для обработки задач
    num_workers = 3
    workers = [asyncio.create_task(worker(worker_id, task_queue, lock)) for worker_id in range(1, num_workers + 1)]

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
