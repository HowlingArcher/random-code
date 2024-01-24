import datetime as dt
import os
import time

# Function to log messages in the log file.
def log(msg):
    # get the current date
    now = dt.datetime.now()
    # only get the date from the now variable
    today = now.date()
    with open(f'{today}_shutdown_pc.log', 'a') as f:
        f.write(f'[{now}] - {msg}\n')

# This function is triggered when the pc is actually shutting down
def shutdown():
    log("Shutting down pc now.")
    os.system('shutdown /s /t 1')

# This function is for when you don't want your monitor to go into sleep mode.
def stayActive(time):
    log("Starting stayActive mode.")
    os.system(f'powercfg -change -monitor-timeout-ac {time}')

# This triggers the shutdown and the stayactive mode if requested.
def shutDownMode(mode, amount, amount1, unit):
    if mode == 'shutdown':
        log(f'Shutdown in {amount1} seconds ({amount}{unit})')
        print(f"Shutting down pc in {amount}{unit}")
        time.sleep(amount1)
        shutdown()
    elif mode == 'active':
        stayActive(amount1)
        log(f'Shutdown in {amount1} seconds ({amount}{unit})')
        print(f"Shutting down pc in {amount}{unit}")
        time.sleep(amount1)
        shutdown()

# This is the main function of the program. It asks the user for all the options needed
def askUser():
    while True:
        try:
            amount = int(input('Enter time: '))
            break
        except ValueError:
            print('Invalid input')
    while True:
        try:
            unit = input('Enter unit (h or m): ')
            if unit == 'h' or unit == 'm':
                break
            else:
                print('Invalid input')
        except ValueError:
            print('Invalid input')
    
    while True:
        try:
            mode = input('Enter mode (shutdown or active): ')
            if mode == 'shutdown' or mode == 'active':
                break
            else:
                print('Invalid input')
        except ValueError:
            print('Invalid input')


    if unit == 'h':
        amount1 = amount * 60 * 60
    elif unit == 'm':
        amount1 = amount * 60

    shutDownMode(mode, amount, amount1, unit)

askUser()