# arduino-face-cam-timer
An arduino project that utilizes a Python Face Recognition library.

In this project, I set up an Arduino with a LCD display and a Piezo buzzer.  With the Python 
[face-recognition](https://github.com/ageitgey/face_recognition) library, I start a timer on the LCD display
when my face is recognized. 

## Main Purpose/Application
Starcraft II is a challenging game.  It requires a lot of multitasking and strategy.  To remind myself
of tasks within the game,  I've programmed the Arduino to activate the buzzer every 10 seconds to remind me to
look at the minimap while playing Starcraft. 

How does the Arduino know when I am playing?  Using a face recognition library, when my face is 
recognized on the webcam, the timer starts.  When I am no longer visible, the timer then stops and resets.
The timer restart again once I my face is recognized again.

## Setup
To run this program, there are several steps that need to be taken other just running `main.py`.

1. `pip` install the requirements.
    1. Note that [face-recognition](https://github.com/ageitgey/face_recognition) is not officially supported
    for Windows machines, but there is a guide on how to install for Windows made by other users.
2. Set up your Arduino with the proper wiring.  See [this image](https://raw.githubusercontent.com/vinceLuong/arduino-face-cam-timer/master/arduino_setup.png)
on how I set up mine.
3. Once the Arduino wiring is done and connected to your comptuer, run the Arduino code found in the
`vincent-led-timer` folder.
4. Run `main.py`.
    1.  Note that the program assumes the Ardiuno is connected to the `COM3` port.  Change `main.py`
    or change your Arduino port to match the code.
    2. You can add your own images to train the facial recognition. See lines [72-91](https://github.com/vinceLuong/arduino-face-cam-timer/blob/master/main.py#L72) 
    on how to add lines of code to train the program.
    3. Also you need a webcam/camera connected to your computer.
