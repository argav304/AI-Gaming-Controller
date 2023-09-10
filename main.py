from ModelRunner import ModelRunner
from GUI import GUI

from threading import Event, Thread
from queue import Queue
from PIL import Image
import customtkinter
import cv2


def update_gui():
    if not frame_queue.empty():
        image = frame_queue.get()
        image = customtkinter.CTkImage(light_image=Image.fromarray(image), dark_image=Image.fromarray(image),
                                       size=(580, 580))
        gui.image_label.image = image
        gui.image_label.configure(image=image)
        gui.image_label.image = image
    gui.after(10, update_gui)

# The camera instance
cap = cv2.VideoCapture(0)

# Frame Queue used to communicate between Main thread where GUI runs and Daemon thread where main_app runs
frame_queue = Queue()

# Event to start the loop in main app
run_event = Event()
run_event.set()  # setting the event


# creating the main_app's thread
main_app_thread = Thread(target=ModelRunner, args=(cap, run_event, frame_queue))
main_app_thread.setDaemon(True)

# Creating instance of the GUI
gui = GUI(cap, run_event)

# starting main_app which captures video feed and does the image recognition as a daemon thread
main_app_thread.start()

# frames updated from the main_app to the GUI using the frame_queue as an intermediate
update_gui()

# Firing up the GUI!
gui.mainloop()
