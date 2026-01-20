# import asyncio

# async def cook(order):
#     print(f"Starting to cook {order}")
#     await asyncio.sleep(4)  # Simulate time-consuming task
#     print(f"{order} is ready!")
#     return f"{order} is served"

# async def main():
#     result1 = await cook("Pasta")
#     result2 = await cook("Pizza")

# asyncio.run(main())


def get_numbers():
    yield 1
    yield 2
    yield 3

gen = get_numbers()
print(gen)  # <generator object ...>

for num in get_numbers():
    print(num)
# Output: 1  2  3
