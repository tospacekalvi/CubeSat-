from machine import Pin, I2C
from bmp280 import BMP280
from mq02 import MQ02
from mpu6050 import MPU6050
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))# Adjust pins as needed
mpu = MPU6050(i2c)
bmp = BMP280(i2c)
mq = MQ02(pin=26)
led = Pin(25,Pin.OUT)





def get_direction_from_accel(accel):
    x = accel['x']
    y = accel['y']
    z = accel['z']

    if x < -0.5:
        return "Left"
    elif x > 0.5:
        return "Right"
    elif y < -0.5:
        return "Backward"
    elif y > 0.5:
        return "Forward"
    elif z < 0.7:
        return "Tilt Down"
    elif z > 1.3:
        return "Tilt Up"
    else:
        return "Stable"

def get_rotation_from_gyro(gyro):
    x = gyro['x']
    y = gyro['y']

    if x > 30:
        return "Rotating Up"
    elif x < -30:
        return "Rotating Down"
    elif y > 30:
        return "Rotating Right"
    elif y < -30:
        return "Rotating Left"
    else:
        return "No major rotation"


while True:
    led.on()
    temp, pressure = bmp.read_compensated_data()
    print("Temperature:", temp, "°C")
    print("Pressure:", pressure, "hPa")
    time.sleep(1)
    print("Air Status:", mq.get_status())
    time.sleep(1)
    accel = mpu.get_accel()
    gyro = mpu.get_gyro()

    direction = get_direction_from_accel(accel)
    rotation = get_rotation_from_gyro(gyro)

    print("📍 Tilt Direction:", direction)
    print("🔁 Rotation:", rotation)
    print("-----------------------------")
    time.sleep(0.8)
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)


