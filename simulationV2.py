#Diego García
#28/03/2023
#Lector de procesos

import simpy
import random

def proceso(creation_time,env,space,num_instructions,RAM:simpy.Container,CPU:simpy.Resource):
    global totalDia

    #Tiempo que tarda en asignar la memoria
    yield env.timeout(creation_time)
    print(f"Se creo el proceso en {env.now}")

    while True:
        if RAM.level>=space:
            RAM.get(space)
            break
        else:
            yield env.timeout(1)

    while num_instructions > 0:
        with CPU.request() as req:
            yield req
            num_instructions -= 3
            yield env.timeout(1)

    print(f"Se termina el proceso en {env.now}")
    RAM.put(space)




env = simpy.Environment()
CPU = simpy.Resource(env, capacity=1)
RAM = simpy.Container(env,capacity=100,init=100)

env.process(proceso(3,env,4,9,RAM,CPU))


env.run()



