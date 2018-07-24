import pygame
import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library

global axis1
ESC1=26  #Connect the ESC1 in this GPIO pin 
ESC2=6  #Connect the ESC1 in this GPIO pin 
ESC3=13  #Connect the ESC1 in this GPIO pin 
ESC4=19  #Connect the ESC1 in this GPIO pin 

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC1, 0) 
pi.set_servo_pulsewidth(ESC2, 0) 
pi.set_servo_pulsewidth(ESC3, 0) 
pi.set_servo_pulsewidth(ESC4, 0) 

max_value = 2000 #change this if your ESC1's max value is different or leave it be
min_value = 1000  #change this if your ESC1's min value is different or leave it be

def control(): 
    print ("Motor starting")
    time.sleep(1)
    speed1 = 1500    
    speed2 = 1500    
    speed3 = 1500    
    speed4 = 1500    
    
    print ("motor initialized")
    while True:
        pi.set_servo_pulsewidth(ESC1, speed1)
        pi.set_servo_pulsewidth(ESC2, speed2)
        pi.set_servo_pulsewidth(ESC3, speed3)
        pi.set_servo_pulsewidth(ESC4, speed4)

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
        
            axis1 = joystick.get_axis( 0 )
            axis2 = joystick.get_axis( 1 )
            axis3 = joystick.get_axis( 2 )
            axis4 = joystick.get_axis( 3 )
            
        ###########################
        if axis1 < -0.1 and axis1 > -0.4:
            speed1 = 1300  # decrementing the speed1 like hell
            speed3 = 1300
            print(axis1)

            print ("speed1 = %d" % speed1)
        elif axis1 > 0.1 and axis1 < 0.4:     
            speed1 = 1700    # incrementing the speed1 like hell
            speed3 = 1700
            print ("speed1 = %d" % speed1)
            print(axis1)
            
        elif axis1 > 0.4:     
            speed1 = 2000  # incrementing the speed1 like hell
            speed3 = 2000  # incrementing the speed1 like hell
            print ("speed1 = %d" % speed1)
            print(axis1)
            
        elif axis1 < -0.4:     
            speed1 = 1000  # incrementing the speed1 like hell
            speed3 = 1000  # incrementing the speed1 like hell
            print ("speed1 = %d" % speed1)
            print(axis1)

        else:
            speed1 = 1500
            speed3 = 1500
            print ("axis1 =0")
            print(axis1)
            print ("axis1 = %d" % axis1)
        ###########################
        if axis2 < -0.1 and  axis2 > -0.4:
            speed2 = 1300  # decrementing the  speed2 like hell
            speed4 = 1300  # decrementing the  speed2 like hell
            print( axis2)

            print (" speed2 = %d" %  speed2)
        elif axis2 > 0.1 and  axis2 < 0.4:     
            speed2 = 1700    # incrementing the  speed2 like hell
            speed4 = 1700  # decrementing the  speed2 like hell
            print (" speed2 = %d" %  speed2)
            print( axis2)
            
        elif axis2 > 0.4:     
            speed2 = 2000  # incrementing the  speed2 like hell
            speed4 = 2000  # incrementing the  speed2 like hell
            print (" speed2 = %d" %  speed2)
            print( axis2)
            
        elif  axis2 < -0.4:     
            speed2 = 1000  # incrementing the  speed2 like hell
            speed4 = 1000  # incrementing the  speed2 like hell
            print (" speed2 = %d" %  speed2)
            print( axis2)

        else:
            speed2 = 1500
            speed4 = 1500
            print (" axis2 =0")
            print( axis2)
            print (" axis2 = %d" %  axis2)
            ##########################
        
def calibrate():
    #This is the auto calibration procedure of a normal ESC1
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0)

    print("press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC1, max_value)
        pi.set_servo_pulsewidth(ESC2, max_value)
        pi.set_servo_pulsewidth(ESC3, max_value)
        pi.set_servo_pulsewidth(ESC4, max_value)

        print("press Enter again")
        inp = raw_input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)

            print ("Special tone")
            time.sleep(7)
            print ("Wait for it ....")
            time.sleep (5)
            print ("Im working on it, DONT WORRY JUST WAIT.....")
            pi.set_servo_pulsewidth(ESC1, 0)
            pi.set_servo_pulsewidth(ESC2, 0)
            pi.set_servo_pulsewidth(ESC3, 0)
            pi.set_servo_pulsewidth(ESC4, 0)

            time.sleep(2)
            print ("Arming ESC1 now...")
            pi.set_servo_pulsewidth(ESC1, min_value)
            pi.set_servo_pulsewidth(ESC2, min_value)
            pi.set_servo_pulsewidth(ESC3, min_value)
            pi.set_servo_pulsewidth(ESC4, min_value)

            time.sleep(1)
            print ("See.... uhhhhh")
            control()


            
def arm(): #This is the arming procedure of an ESC1 

    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC1, max_value)
    pi.set_servo_pulsewidth(ESC2, max_value)
    pi.set_servo_pulsewidth(ESC3, max_value)
    pi.set_servo_pulsewidth(ESC4, max_value)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC1, min_value)
    pi.set_servo_pulsewidth(ESC2, min_value)
    pi.set_servo_pulsewidth(ESC3, min_value)
    pi.set_servo_pulsewidth(ESC4, min_value)
    time.sleep(1)
    control()
    
def stop(): #This will stop every action your Pi is performing for ESC1 ofcourse.
    pi.set_servo_pulsewidth(ESC1, 0)
    pi.set_servo_pulsewidth(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3, 0)
    pi.set_servo_pulsewidth(ESC4, 0)
    pi.stop()

# -------- Main Program Loop -----------

pygame.init()
done = False
pygame.joystick.init()

while done==False:
    calibrate()
    arm()
    control()

stop()
pygame.quit ()
