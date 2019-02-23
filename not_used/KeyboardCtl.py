from pynput.keyboard import Key, Listener


def on_press(key):
    if key == 'w':
        print 'forward'
    elif key == 'a':
        print 'left'
    elif key == 's':
        print 'backward'
    elif key == 'd':
        print 'right'


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


# try:
#     my_car = HBrige.Tank()
#     print('listening')
#     while live:
#         try:
#             if keyboard.is_pressed('q'):  # if key 'q' is pressed
#                 print('You Pressed A Key!')
#                 break  # finishing the loop
#             else:
#                 pass
#         except:
#             break
# finally:
#     HBrige.GPIO.cleanup() # this ensures a clean exit