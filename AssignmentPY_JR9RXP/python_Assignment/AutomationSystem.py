from SmartLight import SmartLight
from Thermostat import Thermostat
from SecurityCamera import SecurityCamera

# Custom exception class for automation system errors
class AutomationError(Exception):
    """Custom exception class for automation system errors."""
    pass

class AutomationSystem:
    def __init__(self):
        # Constructor for the AutomationSystem class.
        # It initializes an empty list to store devices.
        self.devices = []

    def add_device(self, device):
        # Adds a device to the automation system.
        if not hasattr(device, 'device_id'):
            raise AutomationError("Device must have a 'device_id' attribute.")
        self.devices.append(device)
        print(f"Device {device.device_id} added to the automation system.")
        device.automation_system = self

    def discover_devices(self):
        # Discovers and prints information about devices in the automation system.
        print("Discovering devices...")
        for device in self.devices:
            print(f"Device ID: {device.device_id}, Type: {type(device).__name__}")

    def run_simulation(self):
        # Runs the simulation for the automation system.
        print("Running simulation...")
        for device in self.devices:
            try:
                self._process_device_actions(device)
            except AutomationError as e:
                print(f"Error during simulation: {e}")

    def _process_device_actions(self, device):
        # Processes actions for different types of devices.
        if isinstance(device, SmartLight) and device.status == "on":
            self._handle_smart_light_actions(device)
        elif isinstance(device, Thermostat) and device.status == "off":
            self._handle_thermostat_actions()

    def _handle_smart_light_actions(self, light):
        # Handles actions for smart lights.
        if light.brightness < 50:
            self._activate_camera_infrared()

    def _handle_thermostat_actions(self):
        # Handles actions for thermostats.
        if self._are_all_lights_off():
            self._start_camera_recording()

    def _are_all_lights_off(self):
        # Checks if all smart lights are off.
        return all(isinstance(device, SmartLight) and device.status == "off" for device in self.devices)

    def _start_camera_recording(self):
        # Starts recording for security cameras that are on.
        for cam in filter(lambda d: isinstance(d, SecurityCamera) and d.status == "on", self.devices):
            cam.start_recording()

    def _activate_camera_infrared(self):
        # Activates infrared mode for security cameras.
        for cam in filter(lambda d: isinstance(d, SecurityCamera), self.devices):
            cam.enable_infrared()

    def check_and_start_recording(self):
        # Checks conditions and starts camera recording if met.
        try:
            if self._are_all_lights_off() and self._are_all_thermostats_off():
                self._start_camera_recording_and_turn_on()
            else:
                print("Not all lights and thermostats are off.")
        except AutomationError as e:
            print(f"Error when checking conditions: {e}")

    def _are_all_thermostats_off(self):
        # Checks if all thermostats are off.
        return all(isinstance(device, Thermostat) and device.status == "off" for device in self.devices)

    def _start_camera_recording_and_turn_on(self):
        # Starts camera recording and turns on cameras.
        print("Checking conditions...")
        for cam in filter(lambda d: isinstance(d, SecurityCamera), self.devices):
            if cam.status == "off":
                print(f"Turning on Camera {cam.device_id}...")
                cam.turn_on()
            if not cam.recording:
                print(f"Starting recording for Camera {cam.device_id}...")
                cam.start_recording()
            cam.status_var.set(f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")
