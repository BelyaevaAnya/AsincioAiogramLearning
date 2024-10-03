import time
import asyncio


async def notification():
    time.sleep(10)
    print('До доставки осталось 10 минут')


async def main():
    task = asyncio.create_task(notification())
    print('Собираемся обедать')
    print('Едим')


if __name__ == '__main__':
    asyncio.run(main())
