import threading
import time

import busio
from adafruit_pca9685 import PCA9685
from board import SCL, SDA

import rf_gpio


i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 50
mid_duty = 38825
duty_range = 1200

inputs = []


def lerp(a, b, t):
    return a + t*(b - a)

def input_reader():
    global inputs
    
    while 1:
        start_t = time.time()
        
        frames = []
        frame = []
        record = rf_gpio.read_rf(140)
        # print(record)
        for value in record:
            if value > 6000:
                if len(frame) == 17:
                    frames.append(frame)
                frame = []
            else:
                frame.append(value)
        frames = frames[1:-1]
        lengths = [len(frame) for frame in frames[1:-1]]
        meaned_frame = [0]*17
        for frame in frames:
            for i in range(len(meaned_frame)):
                try:
                    meaned_frame[i] += frame[i]/len(frames)
                except:
                    print(frame)
        meaned_frame = [
            str(min(max(int((f - 600)/10), 0), 99)).zfill(2) for f in meaned_frame
            ]
        inputs = [meaned_frame[2*i + 1] for i in range(8)]
        print("  " + "  ".join(inputs))
        
        time.sleep(max(0.2 - (time.time() - start_t), 0))
        # print(time.time() - start_t)

threading.Thread(target=input_reader, args=(), daemon=True).start()

def set_motors_speed(value: int):
    for i in range(4):
        pca.channels[i].duty_cycle = value

if __name__=="__main__":
    set_motors_speed(0)
    time.sleep(1)
    set_motors_speed(mid_duty)
    time.sleep(0.5)
    print("Engaged")
    past_duty_cycle = mid_duty + int(duty_range * (int(inputs[1]) - 50)/100)

    try:
        while 1:
            throttle_value = int(inputs[1])
            
            if throttle_value == 0:
                continue
            duty_cycle = mid_duty + int(duty_range * (throttle_value - 50)/100)
            duty_cycle = int(lerp(past_duty_cycle, duty_cycle, 0.2))
            past_duty_cycle = duty_cycle
                        
            set_motors_speed(duty_cycle)
            time.sleep(0.001)        
            
    except KeyboardInterrupt:
        set_motors_speed(0)

