import random
import math
from ProcessManagerV1 import ProcessManager
import numpy
import simpy

# PARAMETERS
NUMBER_OF_PROCESSES = 10;               # How many process will be spawn in the simulation.
INSTRUCCIONS_PER_PROCCESS = [1, 10];    # Range of instrucctions any proccess can have.
SPACE_PER_PROCESS = [1, 10];            # Range of spaces any process can require.
PROCESS_CREATION_INTERVAL = 10.0;       # Sets possible values 
CPU_SPEED = 3;                          # Instruccions executed per cycle.
CPU_CORES = 1;                          # How many process a CPU can handle at one cycle.
RAM_CAPACITY = 100;                     # Number of proccess RAM can store.
WAITING_IO_SIGNAL = 1;                  # 1 Means this process should move to I/O
IO_TIME = [1,3];                        # Range of time any process can wait for I/O signals.
RANDOM_SEED = 10                        # Dictates how random behaviour will act.

# DATA
execution_time_history = []             # Stores all the times the proc took.

def program_process (
    env:simpy.Environment, 
    id:int,  
    num_instructions:int, 
    space:int ,
    creationTime:int, 
    processManager : ProcessManager):
    """ Program process definition.

    Args:
        env (simpy.Environment): Simulation environment.
        id (int): Process ID.
        num_instructions (int): Number of instructions to execute.
        space (int): Space this process will require on RAM.
        creationTime (int): When this process will spawn on simulation time.
        processManager (ProcessManager): Process manager.
    """
    global execution_time_history
    
    # SPAWN
    yield env.timeout(creationTime);
    print(f"Process {id} spawned at {env.now} with {num_instructions} instructions.");

    # ASK FOR STORAGE
    yield env.process(processManager.getSpace( id, space));
    # ASK FOR CPU EXECUTION.
    yield env.process(processManager.execute( id, num_instructions));
    # FREE ALOCATED SPACE
    yield env.process(processManager.freeSpace(id, space))
    # TERMINATE
    print(f"Process {id} FINISHED in {env.now} took {env.now - creationTime}");
    execution_time_history.append(env.now - creationTime)
    

def setup (env: simpy.Environment, number_of_processes: int, processManager:ProcessManager):
    """ Prepares an environment with procces.

    Args:
        env (simpy.Environment): Simulation environment.
        number_of_processes (int): Process that will be instantiated during simulation.
        processManager (ProcessManager): ProcessManager that will control how process will interact with resources.
    """
    for i in range(NUMBER_OF_PROCESSES):
        creation_time = math.ceil(random.expovariate(1/PROCESS_CREATION_INTERVAL))
        num_instructions = random.randint(*INSTRUCCIONS_PER_PROCCESS)
        space = random.randint(*SPACE_PER_PROCESS)
        env.process(program_process(env, i, num_instructions, space, creation_time, processManager))

if __name__ == "__main__":
    env = simpy.Environment()
    random.seed(RANDOM_SEED)
    process_manager = ProcessManager(env, RAM_CAPACITY, CPU_CORES, CPU_SPEED, IO_TIME)
    setup(env, NUMBER_OF_PROCESSES, process_manager)
    env.run()
    
    # STATISTICS
    average = numpy.average(execution_time_history)
    std_deviation = numpy.std(execution_time_history)
    print(f"\n\nAverage execution time: {average} \n"
        + f"Std. deviation of execution time: {std_deviation}")


