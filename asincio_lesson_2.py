import time
import asyncio


async def get_temp():
    print('Первое показание')
    await asyncio.sleep(2)
    print('25 C*')


async def get_pres():
    print('Второе показание')
    await asyncio.sleep(4)
    print('101 kPa')


async def main():
    print('Старт')
    task1 = asyncio.create_task(get_temp())
    task2 = asyncio.create_task(get_pres())
    await task1
    await task2
    print('Финиш')


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    finish = time.time()
    print(f'Рабочее время = {round(finish - start, 2)} секунды')
