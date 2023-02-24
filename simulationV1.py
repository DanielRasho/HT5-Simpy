import random
import simpy;

# Setting requirements.
numProcesses = 3;
numInstructionsRange = [1, 10]

# Setting up Environment
env = simpy.Environment();
# Memoria -> RecursoLimitado
# Procesador -> RecursoIlimitado

# Process Definition.
def process(env:simpy.Environment, numInstruccions:int):
    pass;

# Processes declaration
for i in range(numProcesses):
    env.process(process(env, random.randint()))
    
env.run();







