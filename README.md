# **Syracuse University CSE 491 Senior Design Project**

Source code to facilitate manual control, path-finding/travel and video/image processing of Robomaster Tello DJI Drone.


**Logging Categories**
    
    DEBUG - Detailed information, typically of interest only when diagnosing problems.
    
    INFO - Confirmation that things are working as expected.
    
    WARNING - An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
    
    ERROR - Due to a more serious problem, the software has not been able to perform some function.
    
    CRITICAL - A serious error, indicating that the program itself may be unable to continue running.

**DJITelloPy**

We used a forked version of damiafuentes/[DJITelloPy](https://github.com/damiafuentes/DJITelloPy).

Our version: [iamapez/DJITelloPy](https://github.com/iamapez/DJITelloPy)

**How to Run**

`python main.py`

Depending on the run configuration, the code can currently do multiple operations. Currently:
1. Attempt a connection to the drone. Must be on the same network as the drone.
2. Start the periodic state logger thread. (log state information every state_logging_interval).
3. Pre-flight actions
4. Flight
5. Land
6. Exit safely
