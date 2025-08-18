from mq02 import MQ02
import time

mq = MQ02(pin=26)  # Use GP26 = ADC0 on Raspberry Pi Pico

while True:
    print("Status:", mq.get_status())
    time.sleep(2)
