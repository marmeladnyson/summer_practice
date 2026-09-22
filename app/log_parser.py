import asyncio
from collections import Counter
from pathlib import Path


ERROR_CODES = (404, 405, 409, 422, 503)


async def error_404(text: str, counters: Counter[int]) -> None:
    if "404" in text:
        counters[404] += 1


async def error_405(text: str, counters: Counter[int]) -> None:
    if "405" in text:
        counters[405] += 1


async def error_409(text: str, counters: Counter[int]) -> None:
    if "409" in text:
        counters[409] += 1


async def error_422(text: str, counters: Counter[int]) -> None:
    if "422" in text:
        counters[422] += 1


async def error_503(text: str, counters: Counter[int]) -> None:
    if "503" in text:
        counters[503] += 1


async def count_errors(path: str | Path = "app.log") -> Counter[int]:
    counters: Counter[int] = Counter()
    handlers = (error_404, error_405, error_409, error_422, error_503)

    with Path(path).open(encoding="utf-8") as log_file:
        for line in log_file:
            await asyncio.gather(*(handler(line, counters) for handler in handlers))

    return counters


async def main() -> None:
    print("Начало работы скрипта")
    counters = await count_errors()
    for code in ERROR_CODES:
        print(f"ERROR {code}: {counters[code]}")


if __name__ == "__main__":
    asyncio.run(main())