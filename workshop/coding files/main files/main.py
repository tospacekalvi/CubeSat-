
from machine import Pin, I2C
from bmp280 import BMP280
from mq02 import MQ02
from mpu6050 import MPU6050
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))

mpu = MPU6050(i2c)
bmp = BMP280(i2c)
mq = MQ02(pin=26)

led = Pin(25, Pin.OUT)


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

    time.sleep(0.2)

    print("Air Status:", mq.get_status())
    time.sleep(0.2)

    # Scaled sensor readings
    accel = mpu.get_accel()
    gyro = mpu.get_gyro()

    # Raw gyroscope readings
    gyro_raw = {
        'x': mpu.read_raw_data(0x43),
        'y': mpu.read_raw_data(0x45),
        'z': mpu.read_raw_data(0x47)
    }

    direction = get_direction_from_accel(accel)
    rotation = get_rotation_from_gyro(gyro)

    print("Accelerometer:", accel)
    print("Gyroscope (°/s):", gyro)

    print("Gyroscope Raw X:", gyro_raw['x'])
    print("Gyroscope Raw Y:", gyro_raw['y'])
    print("Gyroscope Raw Z:", gyro_raw['z'])

    print("Tilt Direction:", direction)
    print("Rotation:", rotation)

    print("-----------------------------")

    time.sleep(0.2)

    led.on()
    time.sleep(0.2)

    led.off()
    time.sleep(0.2)

