import random

def sensor_data():
    vlaznost = random.randint(20,70)
    ph = random.randint(2,13)
    light = random.randint(100,500)

    return vlaznost, ph, light
