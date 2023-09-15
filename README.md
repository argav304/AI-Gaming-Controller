# AI Game Controller
---
## Description

A Gaming Controller which works by utilizing a camera or webcam, this controller system captures the player's movements and translates them into corresponding keyboard key clicks, providing a unique and immersive gameplay experience.

Currently it takes two actions:

 * **Throttle Pull** : equal to pressing and holding down UP arrow key  
   With a closed fist, knuckles facing to the camera pull up aligning axis of wrist
   
 * **Throttle Release** : equal to releasing the UP key if already held down.
   The action is the opposite of applying the throttle.
   
Turning is done as:   
   With two hands along line facing camera, tilt sideways. right hand below for a right turn, vice-versa.  
   
   Left Turn : equal to pressing and holding down LEFT arrow key  
   Right Turn : equal to pressing and holding down RIGHT arrow key  
   
## Dependencies

This project was built on Python 3.8.10 in Windows 10. It's dependencies are:

   * Tensorflow 2.12.0
   * PyAutoGUI 0.9.54
   * MediaPipe 0.10.1
   * OpenCV-python 4.8.0.74
   * Custom Tkinter 5.2.0
     
Tensorflow is used to compile the model. MediaPipe is used to get pose and hand landmarks from video feed. OpenCV is used to view the actual feed. PyAutoGUI is used to convert action predictions to key clicks. 
Custom Tkinter was chosen to build the GUI.

Incase you want to work with the notebook files to work on the model, install **Jupyter Notebook** and **SciKit-Learn**
You can see online resources on how to open the project folder in Jupyter Notebook.

## Setup and Running 

Clone the project into a folder, and create a new environment using [VENV](https://docs.python.org/3/library/venv.html). Alternatively, you could use the IDE's inbuilt feature to create one.
Install the above dependencies using pip

```
pip install tensorflow opencv-python mediapipe pyautogui customtkinter
```
After this open up the project with any IDE and run the **main.py** file, it should start up the application. 
The section below shall detail the use of the GUI which is very simple.

## GUI

<p align="center">
 <img src="https://github.com/argav304/AI-Gaming-Controller/assets/51917179/39ac34ed-59c8-49c8-ba4a-8d686079082c" width="744" height="419"/>
</p>


*  The **START** button is to allow the action recognition model to run. The mediapipe model will
   always run but to start the action recognition model you click **START**.
*  The **KEYS ON** switch allows the action recognitions which are predicted by the model to be converted to 
   the corresponding key click.

---

DISCLAIMER : This thing works on webcam feed, So you would need one. Also, I do not collect any private data.

---
Check out releases section for latest release.
This is concerning release v2.0.0
