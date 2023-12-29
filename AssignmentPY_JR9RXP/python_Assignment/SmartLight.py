class SmartLight:
    """Represents a smart light with adjustable brightness and motion detection capabilities."""

    DEFAULT_BRIGHTNESS = 90  # Default brightness level when the light is turned on

    def __init__(self, device_id, automation_system):
        """Initialize the smart light with a unique device ID and a reference to an automation system."""
        self.device_id = device_id
        self.status = "off"  # Initial status of the light is off
        self.brightness = 0  # Initial brightness is set to 0
        self.automation_system = automation_system  # Reference to the automation system managing this light
        self.status_var = None  # GUI variable to display status, initially set to None

    def _update_status(self, status=None, brightness=None):
        """Private method to update the light's status and brightness."""
        if status is not None:
            self.status = status
        if brightness is not None:
            self.brightness = brightness

        # Create a message reflecting the current status and brightness
        message = f"SmartLight {self.device_id} - Status: {self.status.capitalize()}, Brightness: {self.brightness}%"
        print(message)

        # Update the status variable for GUI, if set
        if self.status_var:
            self.status_var.set(message)

    def turn_on(self):
        """Turns on the smart light to the default brightness."""
        self._update_status(status="on", brightness=self.DEFAULT_BRIGHTNESS)
        print(f"SmartLight {self.device_id} is now on.")

    def turn_off(self):
        """Turns off the smart light and resets its brightness to 0."""
        self._update_status(status="off", brightness=0)
        print(f"SmartLight {self.device_id} is now off.")

        # Trigger automation system's check for recording, if applicable
        if self.automation_system:
            try:
                self.automation_system.check_and_start_recording()
            except Exception as e:
                print(f"Error during automation system recording for SmartLight {self.device_id}: {e}")

    def adjust_brightness(self, brightness):
        """Adjusts the brightness of the smart light."""
        brightness = int(brightness)  # Ensure brightness value is an integer
        self._update_status(brightness=brightness)
        print(f"Brightness of SmartLight {self.device_id} adjusted to {brightness}%.")

    def set_brightness(self, brightness):
        """Sets the brightness of the light if it's on and within valid range."""
        if 0 <= brightness <= 100:
            if self.status == "on":
                self._update_status(brightness=brightness)
                print(f"Brightness of SmartLight {self.device_id} set to {brightness}%.")
            else:
                print(f"SmartLight {self.device_id} is off. Cannot adjust brightness.")
        else:
            print(f"Invalid brightness level: {brightness}. Must be between 0 and 100.")

    def detect_motion(self):
        """Detects motion and turns the light on if it's currently off."""
        print(f"Motion detected by SmartLight {self.device_id}.")
        if self.status == "off":
            self.turn_on()

    def toggle_light(self):
        """Toggles the smart light on or off."""
        if self.status == "off":
            self.turn_on()
        else:
            self.turn_off()
