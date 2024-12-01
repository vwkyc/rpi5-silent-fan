import time
import os
from pathlib import Path
# this script is for Raspberry Pi 5 it is preconfigured for quiet operation
def find_pwmfan_path():
    # Look for the PWM fan hwmon path
    hwmon_paths = list(Path('/sys/class/hwmon').glob('hwmon*'))
    for path in hwmon_paths:
        try:
            with open(path / 'name', 'r') as f:
                if 'pwmfan' in f.read().strip():
                    return path
        except:
            continue
    return None

def get_cpu_temp():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            return float(f.read()) / 1000.0
    except Exception as e:
        print(f"Error reading temperature: {str(e)}")
        return 0

class RPi5FanControl:
    def __init__(self):
        self.hwmon_path = find_pwmfan_path()
        if self.hwmon_path is None:
            raise Exception("Could not find PWM fan control path")
        
        self.enable_path = self.hwmon_path / 'pwm1_enable'
        self.target_path = self.hwmon_path / 'pwm1'
        
        # Verify paths exist
        if not self.enable_path.exists() or not self.target_path.exists():
            raise Exception(f"Required fan control files not found at {self.hwmon_path}")
        
    def set_fan_speed(self, percent):
        try:
            # Enable manual control (1 = manual mode)
            with open(self.enable_path, 'w') as f:
                f.write("1")
            
            # Set fan speed (0-255)
            speed_value = int(255 * (percent / 100))
            with open(self.target_path, 'w') as f:
                f.write(str(speed_value))
            return True
        except Exception as e:
            print(f"Error setting fan speed: {str(e)}")
            return False

def calculate_fan_speed(temp):
    if temp < 60:
        return 0    # Off
    elif temp < 65:
        return 20   # 20% speed - very quiet
    elif temp < 70:
        return 30   # 30% speed - moderate
    elif temp < 75:
        return 40   # 40% speed
    elif temp < 80:
        return 50   # 50% speed
    elif temp < 85: 
        return 65   # 65% speed
    else:
        return 90  # 90% speed

def main():
    try:
        fan_control = RPi5FanControl()
        print("Starting Raspberry Pi 5 fan control. Press CTRL+C to exit.")
        last_speed = -1  # To ensure we print the first speed change
        
        while True:
            temp = get_cpu_temp()
            speed_percent = calculate_fan_speed(temp)
            
            # Only update and print if the speed has changed
            if speed_percent != last_speed:
                success = fan_control.set_fan_speed(speed_percent)
                if success:
                    print(f"CPU Temp: {temp:.1f}°C, Fan Speed: {speed_percent}%")
                last_speed = speed_percent
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Details for debugging:")
        hwmon_path = find_pwmfan_path()
        if hwmon_path:
            print(f"PWM fan path found at: {hwmon_path}")
            print("Available files:")
            for file in hwmon_path.glob('*'):
                print(f"  {file.name}")

if __name__ == "__main__":
    main()
