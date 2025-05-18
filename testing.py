import asyncio


async def foo() -> int:
    await asyncio.sleep(0.3)
    return 1


async def bar() -> str:
    await asyncio.sleep(0.2)
    return "bar"


async def baz() -> bool:
    await asyncio.sleep(0.1)
    return True


async def main() -> None:
    baz_result, bar_result, foo_result = await asyncio.gather(baz(), bar(), foo())
    print(foo_result)
    print(bar_result)
    print(baz_result)


if __name__ == "__main__":
    asyncio.run(main())
