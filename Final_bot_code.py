'''
*****************************************************************************************
*
*        		===============================================
*                  Automated Wall Printing System (AWPS) Bot
*        		===============================================
*
*  This script is for the working of AWPS Bot.
*  1. The program will start by calibrating the ESC along with starting and controlling 
*   the speed of EDF.
*  2. Then the bot takes the movement commands and performs the specified task. 
*
*  Note :- Make sure to not connect the battery to EDF's before calibrating it
*
*
*
*
*****************************************************************************************
'''

# Team ID:			[ Group 33 ]
# Group Member List:		[ Shashwat Gupta ]
#                           [ Prashun Pandey ]
#                           [ Goutham ]
#                           [ Abhay ]
#                           [ Prashant ]
#                           [ Harish ]
# Filename:			Final_bot_code.py
# Functions: manual_drive(), calibrate(), control(), stop() {For EDF's}; 
#            Forward(), Backward(), Rotate_right(), Rotate_left(), Pause(), Stop() {For movement of Bot}; 
#            distance() {For Ultrasonic Sensor}

# Make sure your battery is not connected if you are going to calibrate it at first.

######################################## IMPORT MODULES ########################################

import os     #importing os library so as to communicate with the system
import cv2      #importing openCV library for image processing
import numpy as np  ##importing numpy library for the usage of arrays in image processing
import time   #importing time library to make Rpi wait
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # If this delay is removed we will get an error
import pigpio #importing GPIO library
import RPi.GPIO as GPIO

################################################################################################

'''=========================================================================================='''

######################################## DEFINING PINS #########################################

GPIO.setmode(GPIO.BCM) #GPIO Mode (BOARD / BCM)

ESC=2 #Connect the ESC in this GPIO pin
servoPIN1 = 3 #Connect the Servo Motor in this GPIO pin
servoPIN2 = 4 #Connect the Servo Motor in this GPIO pin
servoPIN3 = 5 #Connect the Servo Motor in this GPIO pin
servoPIN4 = 6 #Connect the Servo Motor in this GPIO pin
TRIGGER = 7 #Connect the Ultrasonic Sensor(TRIGGER) in this GPIO pin
ECHO = 8 #Connect the Ultrasonic Sensor(ECHO) in this GPIO pin

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0) #Pulsewidth used for EDF's

#Set GPIO direction (IN / OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(servoPIN1, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)
GPIO.setup(servoPIN3, GPIO.OUT)
GPIO.setup(servoPIN4, GPIO.OUT)

#Set the frequency for PWM signal
p1 = GPIO.PWM(servoPIN1, 50)
p2 = GPIO.PWM(servoPIN2, 50)
p3 = GPIO.PWM(servoPIN3, 50)
p4 = GPIO.PWM(servoPIN4, 50)

vid = cv2.VideoCapture(1) # define a video capture object

##################################################################################################

'''============================================================================================='''

###################################### FUNCTIONS FOR EDF'S  ######################################

##### These are the functions to set up the ESC and the brushless motor and for their usage #######

##################################################################################################

def manual_drive():
    
    """
    Purpose:
    ---
    This function could be used for programming and controlling the speed of EDF's manually   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    manual_drive()

    """

    print ("You have selected manual option so give a value between 0 and your max value")    
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        else:
            pi.set_servo_pulsewidth(ESC,inp)
                
def calibrate():
    
    """
    Purpose:
    ---
    This function works as the on start set up for EDF's.  

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    calibrate()

    """

    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(12)
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print ("Arming ESC now...")
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print ("EDF Started Working")
            control() # You can change this to any other function you want
            
def control():
    
    """
    Purpose:
    ---
    This function is used for controlling the speed of EDF's   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    control()

    """

    print ("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 1500    # change your speed if you want to.... it should be between 700 - 2000
    print ("Controls for increasing or decreasing the speed of EDF's are as follows :- \n") 
    print("a - decrease speed \n") 
    print("d - increase speed \n") 
    print("q - decrease a lot of speed \n") 
    print("e - increase a lot of speed \n")
    print("p - proceed to further steps \n")
    print("manual - to control the speed manually \n")
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = input()
        
        if inp == "q":
            speed -= 100    # decrementing the speed by a lot
            print ("speed = %d" % speed)
        elif inp == "e":    
            speed += 100    # incrementing the speed by a lot
            print ("speed = %d" % speed)
        elif inp == "d":
            speed += 10     # incrementing the speed 
            print ("speed = %d" % speed)
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print ("speed = %d" % speed)
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp =='p':
            break
        else:
            print ("Please press only a,q,d or e")
    
def stop():
    
    """
    Purpose:
    ---
    This function is used for stopping the EDF's  

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    stop()

    """

    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

################################### END OF FUNCTIONS FOR EDF'S ###################################

'''============================================================================================='''

################################# FUNCTIONS FOR MOVEMENT OF BOT  #################################

####################### These are the functions to move the bot on the wall ######################

##################################################################################################

def Forward():
    
    """
    Purpose:
    ---
    This function is used for moving the bot in forward direction on wall.   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    Forward()

    """
    
    p1.ChangeDutyCycle(5)
    p2.ChangeDutyCycle(5)
    p3.ChangeDutyCycle(5)
    p4.ChangeDutyCycle(5)
    time.sleep(0.5)
    
def Backward():
    
    """
    Purpose:
    ---
    This function is used for moving the bot in backward direction on wall.   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    Backward()

    """

    p1.ChangeDutyCycle(7.5)
    p2.ChangeDutyCycle(7.5)
    p3.ChangeDutyCycle(7.5)
    p4.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    
def Rotate_right():
    
    """
    Purpose:
    ---
    This function is used for rotating the bot in right direction on wall.   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    Rotate_right()

    """
    p1.ChangeDutyCycle(5)
    p2.ChangeDutyCycle(7.5)
    p3.ChangeDutyCycle(5)
    p4.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    
def Rotate_left():
    
    """
    Purpose:
    ---
    This function is used for rotating the bot in left direction on wall.   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    Rotate_left()

    """
    p1.ChangeDutyCycle(7.5)
    p2.ChangeDutyCycle(5)
    p3.ChangeDutyCycle(7.5)
    p4.ChangeDutyCycle(5)
    time.sleep(0.5)

def Pause():
    
    """
    Purpose:
    ---
    This function will pause the bot on wall.   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    Pause()

    """
    pi.set_servo_pulsewidth(ESC, max_value)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    time.sleep(0.5)

def Stop():
    
    """
    Purpose:
    ---
    This function will completely stop the bot.   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    Stop()

    """
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)
    p4.ChangeDutyCycle(0)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

############################## END OF FUNCTIONS FOR MOVEMENT OF BOT ###############################

'''============================================================================================='''

########################### DISTANCE CALCULATION FOR ULTRASONIC SENSOR  ###########################

def distance():

    """
    Purpose:
    ---
    This function will found the distance of obstacle with respect to bot.   

    Input Arguments:
    ---
    None

    Returns:
    ---
    None

    Example call:
    ---
    distance()

    """

    # set Trigger to HIGH
    GPIO.output(TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

######################## END OF DISTANCE CALCULATION FOR ULTRASONIC SENSOR ########################

if __name__ == '__main__':
    
    ###################################################
    max_value = 2000 #specifies the ESC's max value
    min_value = 700  #specifies the ESC's min value
    ##################################################
    ## NOTE: PLEASE DO NOT make any changes in the code below ##   
    
    try:   

        calibrate()

        ret, frame = vid.read()

        print("The EDF had been calirated \n")
        print("The keywords for controlling the bot are as follows :- \n")
        print("w-Forward \n")
        print("s-Backward \n")
        print("a-Rotating Left \n")
        print("d-Rotating Right \n")
        print("Space-Pause \n")
        print("Enter-Stop \n")

        while True:
            img_arr = np.array(frame)
            h, w, channels = img_arr.shape
            lower = np.array([86, 31, 4])
            upper = np.array([220, 88, 50])
            mask = cv2.inRange(img_arr, lower, upper)
            output = cv2.bitwise_and(img_arr, img_arr, mask=mask)

            left_part = output[:, :(w//2)]
            right_part = output[:, (w//2): ]
            upper_part = output[:(h//2), :]
            lower_part = output[(h//2):, :]
            
            cv2.imshow('frame', output)

            number_of_white_pix = np.sum(output == 255)
            number_of_black_pix = np.sum(output == 0)
            
            d = distance()
            inp = input()
            if inp == 'w':
                Forward()
            elif inp == 's':
                Backward()
            elif inp == 'a':
                Rotate_left()
            elif inp == 'd':
                Rotate_right()
            elif inp ==' ':
                Pause()
            elif inp == '':
                Stop()


    except KeyboardInterrupt:
        p1.stop()
        p2.stop()
        p3.stop()
        p4.stop()
        pi.set_servo_pulsewidth(ESC, 0)
        pi.stop()
        vid.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()