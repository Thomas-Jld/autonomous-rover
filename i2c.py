from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import time

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50
mid_duty = 38825
duty_range = 1200

pin = 3
pca.channels[pin].duty_cycle = 0
print("Duty to 0")
time.sleep(3)
pca.channels[pin].duty_cycle = mid_duty # int(max_duty*3/100)
print("Duty to mid_duty")
time.sleep(3)

for i in range(1500):
    pca.channels[pin].duty_cycle = mid_duty + int(duty_range * i /10000) # int(max_duty*(3 + i/20)/100)
    print(f"Duty to {int(duty_range * i /10000)}")
    time.sleep(0.01)

pca.channels[pin].duty_cycle = mid_duty

for i in range(1500):
    pca.channels[pin].duty_cycle = mid_duty - int(duty_range * i /10000) # int(max_duty*(3 + i/20)/100)
    print(f"Duty to {- int(duty_range * i /10000)}")
    time.sleep(0.01)

pca.channels[pin].duty_cycle = 0
