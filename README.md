1. **Director:** This file is responsible for interpreting commands.  Commands can either be run interactively or loaded in through a file.  It'll automatically enter interpreted if no file is specified at command line.  The Director object contains both the Data Manager and Sonde Control objects and accesses their methods as directed by the scripts commands.
2. **Data Manager:**  This program is responsible for recording data to files and logging script history.  Not too much going on here.
3. **Sonde Control:** This program is responsible for interfacing with the hardware (both the Sonde (which is a water sensor) and the Roboclaw (which is a motor controller))
4. **Roboclaw:** Library provided by the Roboclaw manufacturer to interface with the roboclaw in python.  I didnt write this.  Take a look at the Sonde control file for how I controlled the roboclaw.  Lastly, it also interfaces with a button mounted on the raspberry pi.

If you want to run the program, run 
```python Director.py optional-scripting-file```
