import threading
import time

import rf_gpio


inputs = []

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

threading.Thread(input_reader()).start()

