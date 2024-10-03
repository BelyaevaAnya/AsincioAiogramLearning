import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1, 6):
        await asyncio.sleep(1 / power)
        print(f'Силач {name} поднял {i}-шар.')
    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task1
    await task2
    await task3


if __name__ == '__main__':
    asyncio.run(start_tournament())

# Силач Pasha начал соревнования.
# Силач Denis начал соревнования.
# Силач Apollon начал соревнования.
# Силач Apollon поднял 1-шар.
# Силач Denis поднял 1-шар.
# Силач Pasha поднял 1-шар.
# Силач Apollon поднял 2-шар.
# Силач Denis поднял 2-шар.
# Силач Apollon поднял 3-шар.
# Силач Pasha поднял 2-шар.
# Силач Denis поднял 3-шар.
# Силач Apollon поднял 4-шар.
# Силач Apollon поднял 5-шар.
# Силач Apollon закончил соревнования.
# Силач Pasha поднял 3-шар.
# Силач Denis поднял 4-шар.
# Силач Denis поднял 5-шар.
# Силач Denis закончил соревнования.
# Силач Pasha поднял 4-шар.
# Силач Pasha поднял 5-шар.
# Силач Pasha закончил соревнования.
