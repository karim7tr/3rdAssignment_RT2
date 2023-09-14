from __future__ import print_function

import time
from sr.robot import *



a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""

i=1 #round counter

total_length_list=0 #counter of total golden and silver tokens orgranized 

global check 
check = 0 #turns 1 only if the token is successfully grabbed

global list_silver_tokens  #counter of total silver tokens organized
list_silver_tokens=[]

global list_golden_tokens #counter of total golden tokens organized
list_golden_tokens=[]



def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
	tcode (float): silver token code (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER: #silver token at proximity         
            dist=token.dist
	    rot_y=token.rot_y
	    tcode=token.info.code
    if dist>=100: #no token found at proximity    
	return -1, -1, -1
    else:
   	return dist, rot_y, tcode

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
	tcode (float): golden token code (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD: #golden token at proximity             
            dist=token.dist
	    rot_y=token.rot_y
	    tcode=token.info.code
    if dist>=100: #no token found at proximity       
	return -1, -1, -1
    else:
   	return dist, rot_y, tcode
   	
   	
def grab_silver_token():  
    check=0 #initialize check to 0
    while (check ==0) : #while token is not successfully grabbed
        dist, rot_y, tcode = find_silver_token()
        if ((tcode in list_silver_tokens)==False): #token never touched
           if dist==-1: # if no token is detected, we make the robot turn 
	        print("I don't see any SILVER token!!")
	        turn(+10, 1)
           elif dist <d_th: # if we are close to the token, we try grab it.
                print("Found you Mr.Silver!")
                if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position   
                    list_silver_tokens.append(tcode)
                    print("Gotcha, Silver!, right direction and right orientation")                    
                    check =1                   
	        else:
                    print("Aww, I'm not close enough.")
           elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
                print("Ah, that'll do.")
                drive(20, 0.5)
           elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left 
                print("Left a bit...")
                turn(-2, 0.5)
           elif rot_y > a_th: # if the robot is not well aligned with the token, we move it on the right
                print("Right a bit...")
                turn(+2, 0.5)
        else: #the token detected was already moved by robot then no need to move it again
           check=0
           turn(+10, 1) 
           print("Silver Token already dealt with, keep looking!")  

def reach_golden_token():  
    check=0
    while (check ==0) :
        dist, rot_y, tcode = find_golden_token()        
        if ((tcode in list_golden_tokens)==False): #token never touched
            if dist==-1: # if no token is detected, we make the robot turn 
	        print("I don't see any GOLDEN token!!")
	        turn(+10, 1)
            elif dist <0.5: # it is 0.5 and not d_th because we need to consider the size of the token
                print("Found you Mr.Golden!")
                check =1
	        list_golden_tokens.append(tcode)	        
            elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
                print("Ah, that'll do.")
                drive(20, 0.5)
            elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left 
                print("Left a bit...")
                turn(-2, 0.5)
            elif rot_y > a_th: # if the robot is not well aligned with the token, we move it on the right
                print("Right a bit...")
                turn(+2, 0.5)
        else: #the token detected was already moved by robot then no need to move it again
            check=0 
            turn(+12, 1) 
            print("Golden Token already dealt with, keep looking!")    
    
    
"""Main Code """

print("First thing first, lemme get to the center!")
drive(200, 3) 
while (total_length_list<=10): #while not all boxes were arranged, it is <=10 because in every i round the total_length_list size is increased by 2
    grab_silver_token()
    reach_golden_token()
    R.release() #drop the silver token right next to the golden token
    print("Token released")
    drive(-100, 1.5) #drive back closer to the center
    turn(+4, 1)
    total_length_list=((len(list_silver_tokens))+ len((list_golden_tokens))) #total number of tokens organized so far after i rounds
    print("In Round " +str(i)+", size of silver list is "+str(len(list_silver_tokens))) #check total number of silver tokens organized so far after i rounds
    print(list_silver_tokens) #display the list of silver tokens already organized
    print("In Round " +str(i)+", size of golden list is "+str(len(list_golden_tokens))) #check total number of golden tokens organized so far after i rounds
    print(list_golden_tokens) #display the list of golden tokens already organized
    print("In Round " +str(i)+", size of TOTAL list is "+str(total_length_list)) #check total number of tokens organized so far after i rounds
    i+=1 
print("Mission Accomplished!")    
    
