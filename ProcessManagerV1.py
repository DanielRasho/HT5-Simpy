import simpy
import random


class ProcessManager:
    def __init__(
        self,
        env: simpy.Environment,
        storageSize: int,
        cpu_cores: int,
        cpu_speed: int,
        io_time: list[int],
    ) -> None:
        self.env = env
        self.storage = simpy.Container(env, capacity=storageSize, init=storageSize)
        self.cpu = simpy.Resource(env, capacity=cpu_cores)
        self.cpu_speed = cpu_speed
        self.io_time = io_time

    def getSpace(self, id: int, space):
        while True:
            free_space = self.storage.level
            if free_space > space:
                print(f"Fill {space} spaces in storage.")
                self.storage.get(space)
                break
            else:
                yield self.env.timeout(1)

    def freeSpace(self, id: int, space: int):
        yield self.env.timeout(1)
        self.storage.put(space)
        print(f"Free {space} spaces in storage.")

    def execute(self, id: int, num_instructions: int):
        while num_instructions > 0:
            with self.cpu.request() as req:
                yield req
                num_instructions -= self.cpu_speed
                print(
                    f"Process {id} has {num_instructions} instructions left. {self.env.now}"
                )
                yield self.env.process(self.IO_wait(id))

    def IO_wait(self, id: int):
        if random.randint(0, 1) == 1:
            print("Enter IO waiting.")
            yield self.env.timeout(random.randint(*self.io_time))
        else: 
            yield self.env.timeout(1)
