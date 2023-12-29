# Import necessary device classes and modules
from SmartLight import SmartLight
from Thermostat import Thermostat
from SecurityCamera import SecurityCamera
from AutomationSystem import AutomationSystem
import time

# Custom exception class for simulation errors
class SimulationError(Exception):
    """Custom exception class for simulation errors."""

def run_simulation(automation_system):
    """Runs the simulation loop for the automation system."""
    try:
        while True:
            # Continuously run the simulation for the automation system
            automation_system.run_simulation()
            time.sleep(5)  # Sleep for 5 seconds between simulation iterations
    except KeyboardInterrupt:
        print("Simulation loop interrupted by user.")
    except Exception as e:
        raise SimulationError(f"Error during simulation: {e}")

def setup_devices(home_automation):
    """Sets up and adds devices to the automation system."""
    # Create instances of SmartLight, Thermostat, and SecurityCamera devices
    light1 = SmartLight("Light1", home_automation)
    thermostat1 = Thermostat("Thermostat1", home_automation)
    camera1 = SecurityCamera("Camera1", home_automation)

    # Add the created devices to the automation system
    home_automation.add_device(light1)
    home_automation.add_device(thermostat1)
    home_automation.add_device(camera1)

    return light1, thermostat1, camera1

def simulate_device_behavior(light, thermostat, camera):
    """Simulates initial behavior for devices."""
    # Turn on the light, set its brightness to 40%
    light.turn_on()
    light.set_brightness(40)
    # Turn off the thermostat and turn on the camera
    thermostat.turn_off()
    camera.turn_on()

def main():
    try:
        # Create an instance of the AutomationSystem
        home_automation = AutomationSystem()

        # Set up and add devices to the automation system
        light1, thermostat1, camera1 = setup_devices(home_automation)

        # Discover devices in the automation system
        home_automation.discover_devices()

        # Simulate initial behavior for devices
        simulate_device_behavior(light1, thermostat1, camera1)

        # Run the simulation loop
        run_simulation(home_automation)

    except SimulationError as e:
        print(f"Simulation error: {e}")
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")

if __name__ == "__main__":
    main()
