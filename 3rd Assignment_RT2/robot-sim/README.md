Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

## Exercise
-----------------------------

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

I am proposing you three exercises, with an increasing level of difficulty.
The instruction for the three exercises can be found inside the .py files (exercise1.py, exercise2.py, exercise3.py).

When done, you can run the program with:

```bash
$ python run.py exercise1.py
```

You have also the solutions of the exercises (folder solutions)

```bash
$ python run.py solutions/exercise1_solution.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

### Code Used ###

So in order to collect every silver box with golden one we should order our orders that we mention it before , because here we are talking about logic of doing tasks and in the oher hand if we faced error and all of that happening in the main code

  ### Function  Used ###
* `drive()`:drive forward/backward at a specific speed and delay
* `turn()`:turn right/left at a specific speed and delay
* `find_silver_token()`:function to find the closest silver token
* `grab_silver_token()`: function to track and grab the silver token
* `find_golden_token()`: function to find the closest golden token
* `reach_golden_token()`: function to track golden token

***drive() Pseudocode***

  drive forward with set speed

  delay for a set of seconds

  ***turn() Pseudocode***

turn left or right with set speed 

delay for a set of seconds

***find_silver_token()***

initialize dist to 100

For every token seen by robot
    
    If token distance is less than dist and type of token is silver 
     
      input distance of token to dist 
     
      input rotation about the Y of token to rot_y
     
      input code of token to tcode

   endIf 
    
    If distance is higher than dist 
      
      input -1 to dist 
     
      input -1 to rot_y
      
      input -1 to tcode
      
      exit function
    
    endIf

endFor
***grab_silver_token***
  
initialize check to 0

While check is equal to 0
    
    call find_siler_token 
    
    If code of token is not in the list of already organized silver tokens
        
        If distance of silver token is equal to -1 
            
            print " THERE'S NOT ANY SILVER TOKEN !!!!!!!!!!"
            
            call turn with speed +10 and delay 1 
        
        ElIf distance of silver token is less than the threshold distance
            
            print "THE GOAL IS CLEAR : THE SILVER TOKEN IS HERE !"
            
            If grab call is successful 
                
                add code of the silver token to the list of already organized silver tokens
                
                print ""1st MISSION DONE : WE GOT THE SILVER TOKEN !!"
                
                set check to 1 
            
            Else 
                
                print THE MISSION NOT DONE  YET ~ ~ ~"
        
        ElIf the y rotation of silver token is less than the +threshold distance and higher than the -threshold distance
                
                print "ALPHA a is getting CLOSER ^ ^ ^"
                
                call drive with speed of 10 and delay of 0.5
        
        ElIf the y rotation of silver token is less than the -threshold 
                
                print ALPHA a is going left - - -"
                
                call turn with speed of -2 and delay of 0.5
        
        ElIf the y rotation of silver token is higher than the +threshold
                
                print "ALPHA a is going right + + +"
                
                call turn with speed of +2 and delay of 0.5
        
        endIf
    
    Else 
        
        set check to 0
        
        call turn with speed of +10 and delay of 1
        
        print "ALPHA a COMPLETE ITS MISSION WITH THIS SILVER TOKEN , SEARCHING MODE ACTIVITED $"
    
    endIf

endWhile

***find_golden_token()***

 
For every token seen by robot
    
    If token distance is less than dist and type of token is golden 
      
      input distance of token to dist 
      
      input rotation about the Y of token to rot_y
      
      input code of token to tcode
    
    endIf 
    
    If distance is higher than dist 
      
      input -1 to dist 
      
      input -1 to rot_y
      
      input -1 to tcode
      
      exit function
    
    endIf

endFor

***reach_golden_token()***

initialize check to 0

While check is equal to 0
    
    call find_golden_token 
    
    If code of token is not in the list of already organized golden tokens
        
        If distance of golden token is equal to -1 
            
            print "THERE'S NOT ANY GOLDEN TOKEN !!!!!!!!!!"
            
            call turn with speed +10 and delay 1 
        
        ElIf distance of golden token is less than the threshold distance
            
            print "Found you Mr.Golden!"
            
            set check to 1
            
            add code of the golden token to the list of already organized golden tokens
        
        ElIf the y rotation of golden token is less than the +threshold distance and higher than the -threshold distance
                
                print "ALPHA a is getting CLOSER ^ ^ ^ "
                
                call drive with speed of 20 and delay of 0.5
        
        ElIf the y rotation of golden token is less than the -threshold 
                
                print "ALPHA a is going left - - -"
                
                call turn with speed of -2 and delay of 0.5
        
        ElIf the y rotation of golden token is higher than the +threshold
                
                print "ALPHA a is going right + + + ")
                
                call turn with speed of +2 and delay of 0.5
        
        EndIf
    
    Else 
        
        set check to 0
        
        call turn with speed of +12 and delay of 1
        
        print "ALPHA a COMPLETE ITS MISSION WITH THIS GOLDEN TOKEN , SEARCHING MODE ACTIVITED $"
    
    EndIf

EndWhile