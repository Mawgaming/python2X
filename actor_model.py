import asyncio
import queue
import threading
from typing import Any

class Actor:
    def __init__(self):
        self.mailbox = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def send(self, message: Any) -> None:
        self.mailbox.put(message)

    def receive(self, message: Any) -> None:
        raise NotImplementedError("This method should be implemented by subclasses")

    def run(self) -> None:
        while True:
            message = self.mailbox.get()
            self.receive(message)

class Printer(Actor):
    def receive(self, message: str) -> None:
        print(message)

class Counter(Actor):
    def __init__(self):
        super().__init__()
        self.count = 0

    def receive(self, message: str) -> None:
        if message == "increment":
            self.count += 1
            print(f"Count: {self.count}")

class AsyncActor:
    def __init__(self):
        self.mailbox = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.run())

    async def send(self, message: Any) -> None:
        await self.mailbox.put(message)

    async def receive(self, message: Any) -> None:
        raise NotImplementedError("This method should be implemented by subclasses")

    async def run(self) -> None:
        while True:
            message = await self.mailbox.get()
            await self.receive(message)

class AsyncPrinter(AsyncActor):
    async def receive(self, message: str) -> None:
        print(message)

class AsyncCounter(AsyncActor):
    def __init__(self):
        super().__init__()
        self.count = 0

    async def receive(self, message: str) -> None:
        if message == "increment":
            self.count += 1
            print(f"Count: {self.count}")

if __name__ == "__main__":
    async def main():
        printer = AsyncPrinter()
        counter = AsyncCounter()

        await printer.send("Hello, Async Actor World!")
        for _ in range(5):
            await counter.send("increment")

    asyncio.run(main())

