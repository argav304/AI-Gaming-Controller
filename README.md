# AI Game Controller
---
## Description

A Gaming Controller which works by utilizing a camera or webcam, this controller system captures the player's movements and translates them into corresponding keyboard key clicks, providing a unique and immersive gameplay experience.

Currently it takes two actions:

 * **Throttle Pull** : equal to pressing and holding down UP arrow key  
   With a closed fist, knuckles facing to the camera pull up aling axis of wrist
   
 * **Throttle Release** : equal to pressing and holding down DOWN arrow key  
   The opposite of throttle apply.
   
Turning is done as:   
   With two hands along line facing camera, tilt sideways. right hand below for a right turn, vice-versa.  
   
   Left Turn : equal to pressing and holding down LEFt arrow key  
   Right Turn : equal to pressing and holding down RIGHT arrow key  
   
## Dependencies

This project was built on Python 3.8.10 in Windows 10. It's dependencies are:

   * Tensorflow 2.12.0
   * PyAutoGUI 0.9.54
   * MediaPipe 0.10.1
   * OpenCV-python 4.8.0.74
     
Tensorflow is used to compile the model. MediaPipe is used to get pose and hand landmarks form video feed. OpenCV is used to view the actual feed. PyAutoGUI is used to convert action predictions to key clicks

Incase you want to work with the notebook files to work on the model, install **Jupyter Notebook** and **SciKit-Learn**
You can see online resources on how to open the project folder in Jupyter Notebook.

# Setup and Running 

Clone the project into a folder, and create a new environment using [VENV](https://docs.python.org/3/library/venv.html). Install the above dependencies using pip

`pip install tensorflow opencv-python mediapipe pyautogui`

After this open up the project with any IDE and run the **main.py** file, it should open an open-cv window. 
* To close the window, **click 'q'**
* To disable keyclicks caused by actions , **click 'f'**
Ofcourse, for these to register you have to select the open-cv windows( mouse click on it) before clicking the **q**/**f** keys.

---
Check out releases section for latest release.
