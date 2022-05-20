import random

def sensor_data():
    vlaznost = random.randint(1,100)
    ph = random.randint(1,7)
    light = random.randint(100,500)

    return vlaznost, ph, light
