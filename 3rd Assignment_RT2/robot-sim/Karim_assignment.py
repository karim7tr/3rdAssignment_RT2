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

O=1 #round counter

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
    """
    
    dist=100
    for token in R.see():
        
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:  #silver token is proximity       
            dist=token.dist
	    rot_y=token.rot_y
	    tcode=token.info.code
    if dist>=100:    #if we didn't found at proximity
	return -1, -1, -1# here looks like there's error in visual studio but if we fixed the code will not work as we want but in this situation it works very well....how ?! idk 
    else:
   	return dist, rot_y, tcode# here looks like there's error in visual studio but if we fixed the code will not work as we want but in this situation it works very well....how ?! idk 

def find_golden_token():
    

    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """

    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:#golden token is proximity           
            dist=token.dist
        rot_y=token.rot_y
        tcode=token.info.code
    if dist>=100: #if we didn't found at proximity
        return -1, -1, -1
    else:
   	    return dist, rot_y, tcode 

 
def grab_silver_token():  
    check=0  #lanch the check to 0
    while (check ==0) : #if it was unsuccessful operation
        dist, rot_y, tcode = find_silver_token()
        if ((tcode in list_silver_tokens)==False): #token NEVER touched!!!!!!
           if dist==-1:  #if no token is detected, robot must turn !!!!!!!! 
            print(" THERE'S NOT ANY SILVER TOKEN !!!!!!!!!! ")
            turn(+10, 1)
           elif dist <d_th: #if the token is closer enough "THE GOAL IS CLEAR " / next step catch the silver token
                print("THE GOAL IS CLEAR : THE SILVER TOKEN IS HERE !") 
                if R.grab():  #This Operator to catch or grab silver token "THIS IS OUR 1st MISSION FOR THE ROBOT"
                    list_silver_tokens.append(tcode)
                    print("1st MISSION DONE : WE GOT THE SILVER TOKEN !!") # Goodjob :,)                   
                    check =1    #realising operation & confermation               
                else: # This is the possibility of error (x_x)  
                    print("THE MISSION NOT DONE  YET ~ ~ ~")
           elif -a_th<= rot_y <= a_th:  #robot in a good way, move forward 
                print("ALPHA a is getting CLOSER ^ ^ ^")
                # we called the robot ALPHA a 
                drive(40, 0.5)
           elif rot_y < -a_th: #the robot's stauts for the  silver token inappropriate, we gonna turn left 
                print("ALPHA a is going left - - -")
                turn(-4, 0.5)
           elif rot_y > a_th: #if it's still inappropriate stauts, we should turn right then :/ 
                print("ALPHA a is going right + + +")
                turn(+4, 0.5)
        else: # 2nd possibility of error (x_x) , the robot finish his mission with this silver token we should find an other one :)
           check=0
           turn(+10, 1) 
           print("ALPHA a COMPLETE ITS MISSION WITH THIS SILVER TOKEN , SEARCHING MODE ACTIVITED $")


def reach_golden_token():  
    check=0
    while (check ==0) :
        dist, rot_y, tcode = find_golden_token()        
        if ((tcode in list_golden_tokens)==False): #new and proper token
            if dist==-1: #if the robot didn't detect any golden token , it sould turn 
                print("THERE'S NOT ANY GOLDEN TOKEN !!!!!!!!!!")
                turn(+10, 1)
            elif dist <0.5: #important note this is 0.5 size of the token & it's not d_th !
                print("THE GOAL IS CLEAR : THE GOLDEN TOKEN IS HERE !") # Perfect ! 
                check =1
                list_golden_tokens.append(tcode)	

            elif -a_th<= rot_y <= a_th: # robot in good position, go directly >>>>>>
                print("ALPHA a is getting CLOSER ^ ^ ^ ")
                drive(40, 0.5) 
            elif rot_y < -a_th: #the robot's stauts for the  silver token inappropriate, we gonna turn left 
                print("ALPHA a is going left - - -")
                turn(-2, 0.5)
            elif rot_y > a_th: #if it's still inappropriate stauts, we should turn right then :/ 
                print("ALPHA a is going right + + + ")
                turn(+2, 0.5)
        else: 
            check=0 
            turn(+12, 1) 
            print("ALPHA a COMPLETE ITS MISSION WITH THIS GOLDEN TOKEN , SEARCHING MODE ACTIVITED $")    
 
 #those are movements of the robot now we gonna make the main which we can order those movements        
            
            
"MAIN CODE"

print("ALPHA a getting the main position ") #position 0
drive(200, 3) 
while (total_length_list<=10): 
    grab_silver_token()
    reach_golden_token()
    R.release() #logic is working here..../ silver token next to the golden token
    print("RELEASING.....")
    drive(-100, 1.5) #back to the main position
    turn(+4, 1)
    total_length_list=((len(list_silver_tokens))+ len((list_golden_tokens))) # total of tokens we have orgnize them in o round
    print("ALPHA a COMPLETE its mission " +str(O)+", still in silver list is "+str(len(list_silver_tokens)))  #show us the number of silver tokens we have organized them
    print(list_silver_tokens) 
    print("ALPHA a COMPLETE its mission " +str(O)+", still in golden list is "+str(len(list_golden_tokens)))  #show us the number of golden tokens we have organized them
    print(list_golden_tokens) 
    print(" ALPHA a COMPLETE its mission " +str(O)+", size of TOTAL list is "+str(total_length_list))  #show us the number of all tokens we have organized them
    O+=1 
print("MISSION DONE + RESPECT ")    
    #K.0