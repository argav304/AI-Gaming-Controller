import customtkinter
from PIL import Image
import cv2

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    start_button_flag = False
    def __init__(self):
        super().__init__()
        #setting up the camera
        self.vid = cv2.VideoCapture(0)
        # configure window
        self.title("AI Game Controller")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (2x3 : row x col)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        # video feed frame( widget )
        self.videofeed_frame = customtkinter.CTkFrame(self)
        self.videofeed_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.label=customtkinter.CTkLabel(self.videofeed_frame)
        self.label.grid(row=0, column=0,rowspan=2,sticky="nsew")
        ret,frame = self.vid.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = customtkinter.CTkImage(light_image=Image.fromarray(frame),dark_image=Image.fromarray(frame),size=(580,580))
        self.label.img_update=image
        self.label.configure(image=image)


        # buttons and switch

        self.start_button = customtkinter.CTkButton(self,width=200,height=100, text="START",fg_color="#00c9a6", hover_color="#00836c", text_color="#ffffff",  font=customtkinter.CTkFont(size=20, weight="bold"), command=self.start_button)
        self.keyoff_switch = customtkinter.CTkSwitch(self,switch_width=100,switch_height=50,text="KEYS ON", text_color="#ffffff",  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.start_button.grid(row=0, column=1, columnspan=2)
        self.keyoff_switch.grid(row=1,column=1)

    def start_button(self):
        self.start_button_flag = not self.start_button_flag
        if not self.start_button_flag:
            self.start_button.configure(text="START",fg_color="#00c9a6", hover_color="#00836c")
        else:
            self.start_button.configure(text="END",fg_color="#ff0052", hover_color="#660021")


if __name__ == "__main__":
    app = App()
    app.mainloop()

