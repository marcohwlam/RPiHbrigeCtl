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
    def __init__(self, step_pin_forward, step_pin_backward, power_pin, power_duty_cycle):
        self.step_pin_forward = step_pin_forward
        self.step_pin_backward = step_pin_backward
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin_forward, GPIO.OUT)
        GPIO.setup(self.step_pin_backward, GPIO.OUT)
        GPIO.setup(power_pin, GPIO.OUT)
        self.power_pwm = GPIO.PWM(power_pin, 180)
        self.power_pwm.start(power_duty_cycle)
        self.power_pwm.ChangeDutyCycle(power_duty_cycle)

    def set_power(self, power_duty_cycle):
        self.power_pwm.ChangeDutyCycle(power_duty_cycle)


class Car:
    def __init__(self):
        self.wheel_left = Wheel(26, 6, 4, 100)
        self.wheel_right = Wheel(13, 5, 17, 100)

    def forward(self, sleep_time):
        GPIO.output(self.wheel_left.step_pin_forward, GPIO.HIGH)
        GPIO.output(self.wheel_right.step_pin_forward, GPIO.HIGH)
        print "forwarding running  motor "
        time.sleep(sleep_time)
        GPIO.output(self.wheel_left.step_pin_forward, GPIO.LOW)
        GPIO.output(self.wheel_right.step_pin_forward, GPIO.LOW)

    def backward(self, sleep_time):
        GPIO.output(self.wheel_left.step_pin_backward, GPIO.HIGH)
        GPIO.output(self.wheel_right.step_pin_backward, GPIO.HIGH)
        print "step_pin_backward running  motor "
        time.sleep(sleep_time)
        GPIO.output(self.wheel_left.step_pin_backward, GPIO.LOW)
        GPIO.output(self.wheel_right.step_pin_backward, GPIO.LOW)

    def turn_left(self, sleep_time):
        GPIO.output(self.wheel_left.step_pin_forward, GPIO.HIGH)
        GPIO.output(self.wheel_right.step_pin_backward, GPIO.HIGH)
        print "step_pin_backward running  motor "
        time.sleep(sleep_time)
        GPIO.output(self.wheel_left.step_pin_forward, GPIO.LOW)
        GPIO.output(self.wheel_right.step_pin_backward, GPIO.LOW)

    def turn_right(self, sleep_time):
        GPIO.output(self.wheel_left.step_pin_backward, GPIO.HIGH)
        GPIO.output(self.wheel_right.step_pin_forward, GPIO.HIGH)
        print "step_pin_backward running  motor "
        time.sleep(sleep_time)
        GPIO.output(self.wheel_left.step_pin_backward, GPIO.LOW)
        GPIO.output(self.wheel_right.step_pin_forward, GPIO.LOW)

    def blocked(self):
        pass

    # def __del__(self):
        # GPIO.cleanup()


try:
    my_car = Car()
    # my_car.forward(10)
    my_car.backward(10)
    # my_car.turn_right(1)
    # my_car.turn_left(1)
finally:
    GPIO.cleanup() # this ensures a clean exit