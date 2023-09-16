from ModelRunner import toggle_key_click_flag, toggle_start_core_flag
from tkinter import CENTER
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class GUI(customtkinter.CTk):
    start_button_flag = False

    def __init__(self, cap, run_event):
        super().__init__()
        # configure window
        self.title("AI Game Controller")
        self.geometry(f"{1100}x{580}")
        self.protocol("WM_DELETE_WINDOW", self.close_event)
        self.iconbitmap('./icon.ico')
        self.cap = cap
        self.run_event = run_event
        self.keyoff_flag = customtkinter.StringVar(value="off")
        # configure grid layout (2x3 : row x col)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # video feed frame( widget )
        self.videofeed_frame = customtkinter.CTkFrame(self)
        self.videofeed_frame.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
        self.image_label = customtkinter.CTkLabel(self.videofeed_frame, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # buttons and switch

        self.start_button = customtkinter.CTkButton(self, width=200, height=100, text="START", fg_color="#00c9a6",
                                                    hover_color="#00836c", text_color="#ffffff",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"),
                                                    command=self.start_button_event)
        self.keyoff_switch = customtkinter.CTkSwitch(self, switch_width=100, switch_height=50, text="KEYS ON",
                                                     text_color="#ffffff",
                                                     font=customtkinter.CTkFont(size=20, weight="bold"),
                                                     command=self.keyoff_event, variable=self.keyoff_flag, onvalue="on",
                                                     offvalue="off")
        self.start_button.grid(row=0, column=2, columnspan=1)
        self.keyoff_switch.grid(row=1, column=2)

    def start_button_event(self):
        self.start_button_flag = not self.start_button_flag
        if self.start_button_flag:
            toggle_start_core_flag(True)
            self.start_button.configure(text="END", fg_color="#ff0052", hover_color="#660021")
        else:
            toggle_start_core_flag(False)
            self.start_button.configure(text="START", fg_color="#00c9a6", hover_color="#00836c")

    def keyoff_event(self):
        if self.keyoff_flag.get() == "on":
            toggle_key_click_flag(True)
        if self.keyoff_flag.get() == "off":
            toggle_key_click_flag(False)

    def close_event(self):
        self.run_event.clear()
        self.cap.release()
        self.destroy()

