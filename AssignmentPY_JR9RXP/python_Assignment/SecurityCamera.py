from datetime import datetime

class SecurityCameraError(Exception):
    """Custom exception for security camera errors."""
    pass

class SecurityCamera:
    def __init__(self, device_id, automation_system):
        # Constructor for the SecurityCamera class.
        # It initializes various attributes of the security camera device.
        self.device_id = device_id
        self.status = "off"
        self.recording = False
        self.infrared = False
        self.automation_system = automation_system
        self.status_var = None

    def turn_on(self):
        """Turns on the security camera."""
        self.status = "on"
        self._update_status_var("turned on")
        self.detect_motion()

    def turn_off(self):
        """Turns off the security camera."""
        self.status = "off"
        self.recording = False
        self.infrared = False
        self._update_status_var("turned off")

    def toggle_camera(self):
        """Toggles the security camera on/off."""
        if self.status == "off":
            self.status = "on"
            self._update_status_var("turned on")
            self.start_recording()  # If you want the camera to start recording when it turns on
        else:
            self.status = "off"
            self.stop_recording()  # Assuming you want the camera to stop recording when it turns off
            self._update_status_var("turned off")

    def toggle_recording(self):
        """Toggles recording mode for the security camera."""
        if self.status == "on":
            self.recording = not self.recording
            action = "recording" if self.recording else "stopped recording"
            self._update_status_var(action)
        else:
            self._log("is off. Cannot toggle recording.")

    def start_recording(self):
        """Starts recording for the security camera."""
        if self.status == "on":
            if not self.recording:
                self.recording = True
                self._update_status_var("recording")
        else:
            self._log("is off. Cannot start recording.")

    def stop_recording(self):
        """Stops recording for the security camera."""
        if self.status == "on":
            if self.recording:
                self.recording = False
                self._update_status_var("stopped recording")
            else:
                self._log("is not recording. Cannot stop.")
        else:
            self._log("is off. Cannot stop recording.")

    def enable_infrared(self):
        """Enables infrared mode for the security camera."""
        if self.status == "on":
            self.infrared = True
            self._update_status_var("infrared enabled")
        else:
            self._log("is off. Cannot enable infrared.")

    def disable_infrared(self):
        """Disables infrared mode for the security camera."""
        if self.infrared:
            self.infrared = False
            self._update_status_var("infrared disabled")
        else:
            self._log("infrared is not enabled. Cannot disable.")

    def detect_motion(self):
        """Detects motion and takes appropriate actions."""
        self._log("detected motion")
        if self.status == "off":
            self.turn_on()
        if not self.recording:
            self.start_recording()

    def _update_status_var(self, action):
        """Update the status variable with the current status and log the action."""
        status_info = f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}"
        self._log(action)
        if self.status_var:
            self.status_var.set(status_info)

    def _log(self, action):
        """Log an action with a timestamp."""
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        full_message = f"{timestamp} SecurityCamera {self.device_id} {action}."
        print(full_message)
