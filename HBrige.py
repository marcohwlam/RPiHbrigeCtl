# Import required libraries
import datetime
import logging
import time
# from sys import stdin
# import sys, json
from datetime import datetime

import RPi.GPIO as GPIO
from socketIO_client import SocketIO, LoggingNamespace

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
        print GPIO.input(4)

    @staticmethod
    def sensor_callback(channel):
        # Called if sensor output goes LOW
        timestamp = time.time()
        stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        print "Sensor LOW " + stamp


class Track:
    def __init__(self, step_pin_forward, step_pin_backward, power_scale):
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
        self.power_scale = power_scale

    def forward(self, power_duty_cycle):
        self.forward_pwm.ChangeDutyCycle(power_duty_cycle * self.power_scale)

    def backward(self, power_duty_cycle):
        self.backward_pwm.ChangeDutyCycle(power_duty_cycle * self.power_scale)

    def set_power_scale(self, power_scale):
        self.power_scale = power_scale


class Tank:
    def __init__(self):
        self.track_right = Track(26, 6, 1)
        self.track_left = Track(5, 13, 0.8)
        self.hallSensorLeft = HallSensor(4)
        # self.hallSensorRight = HallSensor(4)

    def forward(self, sleep_time, power):
        self.track_left.forward(power)
        self.track_right.forward(power)
        print "forwarding running  motor "
        time.sleep(sleep_time)
        self.track_left.forward(0)
        self.track_right.forward(0)

    def backward(self, sleep_time, power):
        self.track_left.backward(power)
        self.track_right.backward(power)
        print "back running  motor "
        time.sleep(sleep_time)
        self.track_left.backward(0)
        self.track_right.backward(0)

    def turn_left(self, sleep_time, power):
        self.track_left.backward(power)
        self.track_right.forward(power)
        print "left running  motor "
        time.sleep(sleep_time)
        self.track_left.backward(0)
        self.track_right.forward(0)

    def turn_right(self, sleep_time, power):
        self.track_left.forward(power)
        self.track_right.backward(power)
        print "right running  motor "
        time.sleep(sleep_time)
        self.track_left.forward(0)
        self.track_right.backward(0)

    def forward_left(self, duty_cyc):
        self.track_left.forward(duty_cyc)
        print "left running  motor "

    def forward_right(self, duty_cyc):
        self.track_right.forward(duty_cyc)
        print "right running  motor "

    def forward_left(self, duty_cyc):
        self.track_left.forward(duty_cyc)
        print "left running  motor "

    def forward_right(self, duty_cyc):
        self.track_right.forward(duty_cyc)
        print "left running  motor "

    def backward_left(self, duty_cyc):
        self.track_left.backward(duty_cyc)
        print "left running  motor "

    def backward_right(self, duty_cyc):
        self.track_right.backward(duty_cyc)
        print "left running  motor "

    def stop(self):
        print "motor stop"
        self.track_left.backward(0)
        self.track_right.backward(0)
        self.track_left.forward(0)
        self.track_right.forward(0)

    # def __del__(self):
    #     GPIO.cleanup()


# def read_in():
#     lines = sys.stdin.readline()
#     return json.loads(lines)


try:
    print ("Initializing Tank")
    my_car = Tank()
    with SocketIO('localhost', 3000, LoggingNamespace) as socketIO:
        while True:
            now = datetime.now()
            socketIO.emit('python-message', now.strftime("%-d %b %Y %H:%M:%S.%f"))
            socketIO.wait(seconds=1)
            print "hi"
    # while True:
    #     try:
    #         cmd = sys.stdin.readline()
    #         # a = sys.stdin.readline()
    #         print cmd
    #     except:
    #         print "unknow cmd"

finally:
    print "finally"
    GPIO.cleanup()  # this ensures a clean exit
