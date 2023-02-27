#Diego García
#28/03/2023
#Lector de procesos

import simpy
import random

def proceso(num,env,lecture_time,procesador):
    global totalDia

    #Tiempo que tarda en leer la instrucción
    yield env.timeout(lecture_time)

    #Momento en que se ejecutó la instrucción
    ejecutar = env.now

    

