import time
import machine

# IR sensor setup
ir_sensor = machine.Pin(17, machine.Pin.IN)  # Example pin number, adjust as needed

# Acceleration sensor setup
accel_sensor = machine.Pin(12, machine.Pin.IN)  # Example pin number, adjust as needed

# Button setup
button_pin = machine.Pin(13, machine.Pin.IN)  # Example pin number, adjust as needed

# Buzzer setup
buzzer_pin = machine.Pin(14, machine.Pin.OUT)  # Example pin number, adjust as needed

# LED setup
led_pin = machine.Pin(16, machine.Pin.OUT)  # Example pin number, adjust as needed

# GPS setup
gps_accuracy = 0  # Example value, adjust as needed

# Define parachute deployment altitude
deployment_altitude = 500  # Example value, adjust as needed

# Define landing altitude
landing_altitude = 5  # Example value, adjust as needed

# Define emergency deployment altitude
emergency_altitude = 200  # Example value, adjust as needed

# Define system status flags
parachute_deployed = False
second_parachute_deployed = False
landing_mode_initiated = False
rocket_failure = False  # Example, actual failure detection needed

# Main loop
while True:
    # Check if the system is under deployment mode
    if button_pin.value() == 1:
        print("System under deployment mode.")

        # Check if altitude is decreasing
        if not ir_sensor.value() and accel_sensor.value():
            print("Altitude is decreasing.")
            
            # Check if other systems have failed
            if rocket_failure:
                print("Rocket failure detected. System remains on standby.")
            else:
                # Deploy the first parachute
                print("Deploying 1st parachute.")
                parachute_deployed = True
                
                # Start the reaction wheel
                print("Starting reaction wheel.")
                
                # Check if first parachute deployment fails
                if not parachute_deployed:
                    print("First parachute deployment failed. Deploying 2nd parachute.")
                    # Deploy the second parachute
                    print("Deploying 2nd parachute.")
                    second_parachute_deployed = True
                    # Check if second parachute deployment fails
                    if not second_parachute_deployed:
                        print("Second parachute deployment failed. Using fins and reaction wheel at max mode.")
                        # Use fins and reaction wheel at max mode
                        print("Using fins and reaction wheel at max mode.")
                
        else:
            print("Altitude is not decreasing or other systems have not failed. Remaining on standby.")
    
    # Check for landing mode initiation
    if not landing_mode_initiated:
        # Check altitude
        altitude = 10  # Example altitude value, should be obtained from sensor
        if altitude <= landing_altitude:
            print("Altitude below landing threshold. Initiating landing mode.")
            landing_mode_initiated = True
            # Activate buzzer
            buzzer_pin.on()

    # Check if altitude is less than 500m under normal operation
    if not parachute_deployed and altitude < deployment_altitude:
        print("Altitude is less than 500m. Deploying 2nd parachute and activating grid mechanism in normal mode.")
        # Deploy the second parachute
        print("Deploying 2nd parachute.")
        second_parachute_deployed = True
        # Activate grid mechanism in normal mode
        print("Activating grid mechanism in normal mode.")

    # Check if altitude is less than 200m for high-speed data logging
    if altitude < emergency_altitude:
        print("Altitude is less than 200m. Starting high-speed data logging.")
        # Start high-speed data logging

    # Check for landing mode initiation
    if altitude < landing_altitude and accel_sensor.value() == 0:
        print("Altitude is less than 5m and accelerometer detects zero velocity. Initiating landing mode.")
        # Initiate landing mode
        # Beep the buzzer
        buzzer_pin.on()
        # Increase GPS accuracy
        gps_accuracy = 1  # Example value for increased accuracy
        # Start blinking the LED light
        for _ in range(10):  # Blink 10 times
            led_pin.on()
            time.sleep(0.5)
            led_pin.off()
            time.sleep(0.5)

    # Check for rocket failure
    if rocket_failure:
        print("Rocket failure detected. System remains on standby.")

    time.sleep(1)  # Adjust sleep time as needed
    
    
    
## EXPLANATION OF THE CODE 
# in this start by checking the altititude if it is below 200m emergency mechanism to be deployed

# if altitude is greater than 200 check button position if pushed that means the system is under deployment mode

# under deployment mode use ir sensor and acceleration sensor to detect if altitude is decreasing or not, if it is decreasing and other systems have failed then stay on stand by

# if decreasing and other systems have not failed deploy the first parachute
# while deploying the first parachute also start the reaction wheel,
# if the deployment of 1st parachute fails immediately deploy the second parachute, and if second parachute deployment fails as well use the fins and reaction wheel at max mode,
# if the first parachute gets succesfully deployed,
# check for altitude again now if it is less than 500 m

# if under normal operation the altitude is less than 500, deploy the second paracute and activate the grid mech in normal mode and keep checking the altitiude,

# once the altitude is below 200m start high speed data  logging,
# and when altitude is less than 5 m and accelerometer detects zero velocity initiate landing mode

# under landing mode, start beeping the buzzer, increase the  accuracy of gps location and start blinking the led light    