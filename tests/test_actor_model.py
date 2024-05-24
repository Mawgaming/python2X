import unittest
import asyncio
from actor_model import Printer, Counter, AsyncPrinter, AsyncCounter

class TestActorModel(unittest.TestCase):
    def test_printer(self):
        printer = Printer()
        printer.send("Hello, Test World!")

    def test_counter(self):
        counter = Counter()
        for _ in range(5):
            counter.send("increment")

class TestAsyncActorModel(unittest.TestCase):
    def test_async_printer(self):
        async def test():
            printer = AsyncPrinter()
            await printer.send("Hello, Async Test World!")

        asyncio.run(test())

    def test_async_counter(self):
        async def test():
            counter = AsyncCounter()
            for _ in range(5):
                await counter.send("increment")

        asyncio.run(test())

if __name__ == '__main__':
    unittest.main()

