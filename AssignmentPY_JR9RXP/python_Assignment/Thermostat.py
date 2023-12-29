class InvalidTemperatureError(Exception): # builtin exception
    """Exception raised when an invalid temperature is set for the thermostat."""
    pass

class Thermostat:
    DEFAULT_TEMPERATURE = 20  # Default temperature set for the thermostat
    MIN_TEMPERATURE = 10  # Minimum allowable temperature
    MAX_TEMPERATURE = 30  # Maximum allowable temperature

    def __init__(self, device_id, automation_system=None):
        """Initialize the thermostat with a device ID and an optional reference to an automation system."""
        self.device_id = device_id
        self.status = "off"  # Initial status of the thermostat is off
        self.temperature = self.DEFAULT_TEMPERATURE  # Set initial temperature to default
        self.automation_system = automation_system  # Reference to the central automation system
        self.status_var = None  # GUI variable to display status, initially set to None

    def _update_status_var(self):
        """Private method to update the status variable with the current status and temperature."""
        if self.status_var is not None:
            status_info = f"Thermostat {self.device_id} - Status: {self.status.capitalize()}, Temperature: {self.temperature}°C"
            self.status_var.set(status_info)
            print(status_info)

    def toggle_thermostat(self):
        """Toggle the thermostat's state between on and off."""
        if self.status == "off":
            self.turn_on()
        else:
            self.turn_off()
        self._update_status_var()

    def turn_on(self):
        """Turn on the thermostat and update its status."""
        self.status = "on"
        self._update_status_var()
        print(f"Thermostat {self.device_id} is now on.")

    def turn_off(self):
        """Turn off the thermostat, reset to default temperature, and update its status."""
        self.status = "off"
        self.temperature = self.DEFAULT_TEMPERATURE
        self._update_status_var()
        print(f"Thermostat {self.device_id} is now off.")

        # Check and start recording in the automation system if necessary
        if self.automation_system:
            try:
                self.automation_system.check_and_start_recording()
            except Exception as e:
                print(f"Error starting recording in automation system: {e}")

    def set_temperature(self, temperature):
        """Set the thermostat's temperature within a valid range if the thermostat is on."""
        try:
            temperature = int(temperature)
            if self.MIN_TEMPERATURE <= temperature <= self.MAX_TEMPERATURE:
                if self.status == "on":
                    self.temperature = temperature
                    self._update_status_var()
                    print(f"Temperature of Thermostat {self.device_id} set to {temperature}°C.")
                else:
                    print(f"Thermostat {self.device_id} is off. Cannot set temperature.")
            else:
                # Raise an error if the temperature is out of bounds
                raise InvalidTemperatureError(f"Temperature must be between {self.MIN_TEMPERATURE}°C and {self.MAX_TEMPERATURE}°C.")
        except ValueError:
            # Handle non-integer temperature inputs
            print(f"Invalid temperature input: {temperature}")
        except InvalidTemperatureError as e:
            # Handle invalid temperature range
            print(e)
