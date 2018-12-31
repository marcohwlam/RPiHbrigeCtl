# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
# GPIO.setmode(GPIO.BCM)
mode = GPIO.getmode()
print " mode =" + str(mode)


class Wheel:
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

class Car:
    def __init__(self):
        self.wheel_left = Wheel(26, 6, 1)
        self.wheel_right = Wheel(13, 5, 0.9)

    def forward(self, sleep_time, power):
        self.wheel_left.forward(power)
        self.wheel_right.forward(power)
        print "forwarding running  motor "
        time.sleep(sleep_time)
        self.wheel_left.forward(0)
        self.wheel_right.forward(0)

    def backward(self, sleep_time, power):
        self.wheel_left.backward(power)
        self.wheel_right.backward(power)
        print "forwarding running  motor "
        time.sleep(sleep_time)
        self.wheel_left.backward(0)
        self.wheel_right.backward(0)

    def turn_left(self, sleep_time, power):
        self.wheel_left.backward(power)
        self.wheel_right.forward(power)
        print "forwarding running  motor "
        time.sleep(sleep_time)
        self.wheel_left.backward(0)
        self.wheel_right.forward(0)

    def turn_right(self, sleep_time, power):
        self.wheel_left.forward(power)
        self.wheel_right.backward(power)
        print "forwarding running  motor "
        time.sleep(sleep_time)
        self.wheel_left.forward(0)
        self.wheel_right.backward(0)

    def blocked(self):
        pass

    # def __del__(self):
        # GPIO.cleanup()


try:
    my_car = Car()
    for i in range(0, 100):
        my_car.forward(0.3, 50)
        my_car.backward(0.2, 50)
    # my_car.turn_right(1)
    # my_car.turn_left(1)
finally:
    GPIO.cleanup() # this ensures a clean exit