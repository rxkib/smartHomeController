import sys  # redirect standard output
import tkinter as tk  # gui package
from tkinter import ttk, scrolledtext  # text in GUI
import random
from SmartLight import SmartLight
from Thermostat import Thermostat
from SecurityCamera import SecurityCamera
from AutomationSystem import AutomationSystem
from datetime import datetime


class SmartHomeGUI(tk.Tk):
    def __init__(self, automation_system):
        super().__init__()
        self.automation_system = automation_system  # Reference to the home automation system
        self.title("Smart Home IoT Automation Simulator")  # Window title
        self.geometry("1000x700")  # Window size
        self.style = ttk.Style(self)  # Tkinter style for widgets
        self.configure_styles()  # Apply styles to widgets

        self.configure_layout()  # Configure the layout of the GUI

        # Redirect standard output to the log text widget
        sys.stdout = TextRedirector(self.log_text)

        self.add_devices_to_frame()  # Add devices to the GUI
        self.add_random_detect_motion_button()  # Add random motion detection button for cameras

    def configure_styles(self):
        # Configure styles for different widgets
        self.style.configure('TFrame', background='black')  # Set main frame background to black
        self.style.configure('TLabel', background='black', foreground='orange', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12), background='white', foreground='black')
        # Set button background to white
        self.style.configure('White.TLabelframe', background='black')  # Background for label frames
        self.style.configure('White.TLabelframe.Label', background='black', foreground='white')  # Background for labels in label frames
        self.style.configure('Device.TButton', font=('Arial', 12), background='orange', foreground='black')  # Button style for device controls
        self.style.configure('Device.Horizontal.TScale', troughcolor='black', sliderbackground='dark black', sliderborderwidth=1)  # Style for sliders

    def configure_layout(self):
        # Configure the main layout of the GUI
        self.main_frame = ttk.Frame(self, style='TFrame')
        self.main_frame.pack(side=tk.TOP, fill="both", expand=True)

        self.log_frame = ttk.LabelFrame(self.main_frame, text="Log")
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, width=40, height=10)
        self.log_text.pack(fill="both", expand=True)

        self.device_control_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.device_control_frame.pack(fill="both", expand=True)

        # Frames for different device types
        self.light_frame = ttk.LabelFrame(self.device_control_frame, text="Smart Lights", style='White.TLabelframe')
        self.thermostat_frame = ttk.LabelFrame(self.device_control_frame, text="Thermostats", style='White.TLabelframe')
        self.camera_frame = ttk.LabelFrame(self.device_control_frame, text="Security Cameras", style='White.TLabelframe')

        self.light_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        self.thermostat_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        self.camera_frame.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")

        # Configure grid weights
        self.device_control_frame.grid_rowconfigure(0, weight=1)
        self.device_control_frame.grid_columnconfigure(0, weight=1)
        self.device_control_frame.grid_columnconfigure(1, weight=1)
        self.device_control_frame.grid_columnconfigure(2, weight=1)

    def add_devices_to_frame(self):
        # Add device controls for each device in the automation system
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight):
                self.setup_device_controls(device, self.light_frame, 'light')
            elif isinstance(device, Thermostat):
                self.setup_device_controls(device, self.thermostat_frame, 'thermostat')
            elif isinstance(device, SecurityCamera):
                self.setup_device_controls(device, self.camera_frame, 'camera')

    def add_random_detect_motion_button(self):
        # Add a button to trigger random motion detection on a security camera
        def random_motion_detect():
            cameras = [device for device in self.automation_system.devices if isinstance(device, SecurityCamera)]
            if cameras:
                random.choice(cameras).detect_motion()
                self.log("Random motion detection triggered.")
        random_motion_button = ttk.Button(self.camera_frame, text="Random Detect Motion", command=random_motion_detect)
        random_motion_button.pack(padx=10, pady=10)

    @staticmethod
    def add_label(frame, text):
        # Add a label to a given frame
        label = ttk.Label(frame, text=text, font=("Bookman Old Style", 12))
        label.pack(pady=5)

    @staticmethod
    def add_button(frame, text, command, style=None):
        # Add a button to a given frame
        if style:
            button = ttk.Button(frame, text=text, command=command, style=style)
        else:
            button = ttk.Button(frame, text=text, command=command)
        button.pack(padx=10, pady=10)
        return button

    @staticmethod
    def add_scale(frame, from_, to, command, initial_value):
        # Add a scale (slider) to a given frame
        scale = ttk.Scale(frame, from_=from_, to=to, command=command)
        scale.set(initial_value)
        scale.pack(padx=10, pady=5)
        return scale

    @staticmethod
    def create_status_var_and_label(frame, initial_value):
        # Create a label with a variable text in a given frame
        status_var = tk.StringVar(value=initial_value)
        status_label = ttk.Label(frame, textvariable=status_var)
        status_label.pack()
        return status_var

    def setup_device_controls(self, device, frame, device_type):
        # Setup controls for a specific device in a specific frame
        SmartHomeGUI.add_label(frame, f"Device: {device.device_id}")
        status_var = SmartHomeGUI.create_status_var_and_label(frame, "")

        device.status_var = status_var
        status_var.set("Status: off, Recording: false, Infrared: false")

        # Add controls based on device type
        if device_type == 'light':
            def toggle_light():
                device.turn_on() if device.status == "off" else device.turn_off()
                status_var.set(f"Status: {device.status}, Brightness: {device.brightness}%")
            def adjust_brightness(val):
                brightness = int(round(float(val)))
                device.set_brightness(brightness)
                status_var.set(f"Status: {device.status}, Brightness: {device.brightness}%")
            SmartHomeGUI.add_button(frame, "Toggle Light", toggle_light)
            SmartHomeGUI.add_scale(frame, 0, 100, adjust_brightness, device.brightness)

        elif device_type == 'thermostat':
            def toggle_thermostat():
                device.toggle_thermostat()
                status_var.set(f"Status: {device.status}, Temperature: {device.temperature}°C")
            def adjust_temperature(val):
                device.set_temperature(int(float(val)))
                status_var.set(f"Status: {device.status}, Temperature: {device.temperature}°C")
            SmartHomeGUI.add_button(frame, "On/Off", toggle_thermostat)
            SmartHomeGUI.add_scale(frame, 10, 30, adjust_temperature, device.temperature)

        elif device_type == 'camera':
            def toggle_camera():
                device.toggle_camera()
                if device.status == "off":
                    device.toggle_recording()
                    device.disable_infrared()
                status_var.set(f"Status: {device.status}, Recording: {device.recording}, Infrared: {device.infrared}")
            def toggle_recording():
                if device.status == "on":
                    device.toggle_recording()
                    status_var.set(f"Status: {device.status}, Recording: {device.recording}, Infrared: {device.infrared}")
            SmartHomeGUI.add_button(frame, "Camera On/Off", toggle_camera, style='Camera.TButton')
            SmartHomeGUI.add_button(frame, "Recording On/Off", toggle_recording, style='Camera.TButton')

    def simulation_loop(self):
        # Loop through devices and apply logic based on their state
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight) and device.status == "on":
                for cam in self.automation_system.devices:
                    if isinstance(cam, SecurityCamera) and cam.status == "on":
                        if device.brightness < 50 and not cam.infrared:
                            cam.enable_infrared()
                            cam.status_var.set(f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")
                            self.log("Infrared enabled.")
                        elif device.brightness >= 50 and cam.infrared:
                            cam.disable_infrared()
                            cam.status_var.set(f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")
                            self.log("Infrared disabled.")
        self.update_device_status()
        self.after(1000, self.simulation_loop)

    def update_device_status(self):
        # This method is responsible for updating the status of devices in a graphical user interface.
        # It iterates through frames (containers) containing widgets, such as labels, and updates them.
        for frame in [self.light_frame, self.thermostat_frame, self.camera_frame]:
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Label) and "textvariable" in widget.keys():
                    # Check if the widget is a label with a text variable and update its tasks.
                    widget.update_idletasks()

    @staticmethod
    def log(message):
        # This static method is used for logging messages with timestamps.
        # It takes a message as input, adds a timestamp to it, and prints it to the console.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)


class TextRedirector:
    def __init__(self, widget):
        # Constructor for TextRedirector class.
        # It takes a GUI widget as input and initializes the widget and buffer attributes.
        self.widget = widget
        self.buffer = ""  # Initialize the buffer attribute

    def write(self, message):
        # This method is responsible for redirecting text output to a GUI widget.
        # It takes a message as input and appends it to the buffer. If a newline character
        # is detected in the message, it adds a timestamp and logs the message to the widget.
        if '\n' in message:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            log_message = f"{timestamp} {self.buffer}{message}"
            self.widget.insert(tk.END, log_message)
            self.widget.see(tk.END)
            self.buffer = ""
        else:
            self.buffer += message

    def flush(self):
        # This method is not used in this implementation, as it's empty.
        pass

# Instantiate devices and automation system
home_automation = AutomationSystem()
light1 = SmartLight("Light1", home_automation)
thermostat1 = Thermostat("Thermostat1", home_automation)
camera1 = SecurityCamera("Camera1", home_automation)

home_automation.add_device(light1)
home_automation.add_device(thermostat1)
home_automation.add_device(camera1)

# Run the GUI
if __name__ == "__main__":
    app = SmartHomeGUI(home_automation)
    app.simulation_loop()
    app.mainloop()
