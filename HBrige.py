import datetime
import logging
import time
from datetime import datetime

import RPi.GPIO as GPIO

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()


# Use BCM GPIO references
# instead of physical pin numbers
# GPIO.setmode(GPIO.BCM)
# mode = GPIO.getmode()
# print " mode =" + str(mode)


class HallSensor:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.sensor_callback)
        print(GPIO.input(4))

    @staticmethod
    def sensor_callback(channel):
        # Called if sensor output goes LOW
        timestamp = time.time()
        stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        print("Sensor LOW " + stamp)


class Track:
    def __init__(self, step_pin_forward, step_pin_backward, power_scale=1.0, min_duty_cycle=30):
        self.step_pin_forward = step_pin_forward
        self.step_pin_backward = step_pin_backward
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin_forward, GPIO.OUT)
        GPIO.setup(self.step_pin_backward, GPIO.OUT)
        self.power_duty_cycle = 0
        self.forward_pwm = GPIO.PWM(step_pin_forward, 1000)
        self.forward_pwm.start(self.power_duty_cycle)
        self.backward_pwm = GPIO.PWM(step_pin_backward, 1000)
        self.backward_pwm.start(self.power_duty_cycle)
        self.power_scale = power_scale * (100 - min_duty_cycle) / 100
        self.min_duty_cycle = min_duty_cycle

    def forward(self, power_duty_cycle):
        if power_duty_cycle == 0:
            self.forward_pwm.ChangeDutyCycle(0)
            return
        self.forward_pwm.ChangeDutyCycle(power_duty_cycle * self.power_scale + self.min_duty_cycle)

    def backward(self, power_duty_cycle):
        if power_duty_cycle == 0:
            self.backward_pwm.ChangeDutyCycle(0)
            return
        self.backward_pwm.ChangeDutyCycle(power_duty_cycle * self.power_scale + self.min_duty_cycle)

    def set_power_scale(self, power_scale):
        self.power_scale = power_scale


class Tank:
    def __init__(self):
        print("Initializing Tank")
        self.track_right = Track(26, 6)
        self.track_left = Track(5, 13)
        self.hallSensorLeft = HallSensor(4)
        # self.hallSensorRight = HallSensor(4)

    def forward(self, sleep_time, power):
        self.track_left.forward(power)
        self.track_right.forward(power)
        print("forward")
        time.sleep(sleep_time)
        self.track_left.forward(0)
        self.track_right.forward(0)

    def backward(self, sleep_time, power):
        self.track_left.backward(power)
        self.track_right.backward(power)
        print("backward")
        time.sleep(sleep_time)
        self.track_left.backward(0)
        self.track_right.backward(0)

    def turn_left(self, sleep_time, power):
        self.track_left.backward(power)
        self.track_right.forward(power)
        print("turn_left")
        time.sleep(sleep_time)
        self.track_left.backward(0)
        self.track_right.forward(0)

    def turn_right(self, sleep_time, power):
        self.track_left.forward(power)
        self.track_right.backward(power)
        print("turn_right")
        time.sleep(sleep_time)
        self.track_left.forward(0)
        self.track_right.backward(0)

    def forward_left(self, duty_cyc):
        self.track_left.forward(duty_cyc)
        print("forward_left")

    def forward_right(self, duty_cyc):
        self.track_right.forward(duty_cyc)
        print("forward_right")

    def backward_left(self, duty_cyc):
        self.track_left.backward(duty_cyc)
        print("backward_left")

    def backward_right(self, duty_cyc):
        self.track_right.backward(duty_cyc)
        print("backward_right")

    def stop(self):
        print("motor stop")
        self.track_left.backward(0)
        self.track_right.backward(0)
        self.track_left.forward(0)
        self.track_right.forward(0)

    def stop_left(self):
        print("motor stop")
        self.track_left.backward(0)
        self.track_left.forward(0)

    def stop_right(self):
        print("motor stop")
        self.track_right.backward(0)
        self.track_right.forward(0)

# try:
#     my_car = Tank()
#     for i in range(0, 100):
#         my_car.forward_left(100)
#         time.sleep(1)
#         my_car.stop()
# #
# finally:
#     print("finally")
#     GPIO.cleanup()  # this ensures a clean exit
