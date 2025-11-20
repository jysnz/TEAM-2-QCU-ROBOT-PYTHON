# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       [Your Name]                                                  #
# 	Created:      [Date]                                                       #
# 	Description:  VEX V5 Competition Template                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# =============================================================================
# 1. ROBOT CONFIGURATION
#    Initialize your devices (Motors, Sensors, Controller) here.
# =============================================================================

# Brain and Controller
brain = Brain()
controller_1 = Controller()

# Motors (Example: 4-Motor Drivetrain)
# Format: Motor(Ports.PORT1, GearSetting.RATIO_18_1, False) 
# "False" = Forward, "True" = Reverse
left_front = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_back  = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_front = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
right_back  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

# Motor Groups (Optional but recommended for easier coding)
left_drive_group = MotorGroup(left_front, left_back)
right_drive_group = MotorGroup(right_front, right_back)

# Mechanism Motors (Intake, Lift, etc.)
intake_motor = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)

# Sensors
inertial = Inertial(Ports.PORT15)

# =============================================================================
# 2. GLOBAL CONSTANTS & VARIABLES
# =============================================================================

# Speed Settings
DRIVE_SPEED = 80
TURN_SPEED = 50
INTAKE_SPEED = 100

# Deadzone (Prevents robot from creeping when joystick is slightly off-center)
DEADZONE = 5

# =============================================================================
# 3. HELPER FUNCTIONS
#    Create reusable functions to keep your code clean.
# =============================================================================

def drive_forward(distance_cm, speed):
    """Moves the robot forward for a set distance."""
    left_drive_group.set_velocity(speed, PERCENT)
    right_drive_group.set_velocity(speed, PERCENT)
    # Note: You will need to calculate turns_per_cm based on your wheel size
    left_drive_group.spin_for(FORWARD, distance_cm, MM, wait=False)
    right_drive_group.spin_for(FORWARD, distance_cm, MM, wait=True)

def turn_right(degrees, speed):
    """Turns the robot right."""
    left_drive_group.set_velocity(speed, PERCENT)
    right_drive_group.set_velocity(speed, PERCENT)
    # Spin directions must be opposite
    left_drive_group.spin_for(FORWARD, degrees, DEGREES, wait=False)
    right_drive_group.spin_for(REVERSE, degrees, DEGREES, wait=True)

# =============================================================================
# 4. COMPETITION FUNCTIONS
# =============================================================================

def pre_autonomous():
    """
    Run this BEFORE the match starts.
    Use this to calibrate gyros, reset encoders, or select auton routines.
    """
    brain.screen.print("Calibrating Inertial...")
    inertial.calibrate()
    
    # Wait for calibration to finish (usually 2-3 seconds)
    while inertial.is_calibrating():
        wait(100, MSEC)
        
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("System Ready!")
    
    # Reset motor encoders
    left_drive_group.reset_position()
    right_drive_group.reset_position()

def autonomous():
    """
    The autonomous period logic.
    """
    brain.screen.print("Running Autonomous")
    
    # Example Routine
    drive_forward(500, DRIVE_SPEED) # Drive 500mm
    wait(200, MSEC)                 # Short pause to settle
    turn_right(90, TURN_SPEED)      # Turn 90 degrees
    
    # Intake example
    intake_motor.spin(FORWARD, 100, PERCENT)

def user_control():
    """
    The driver control period logic.
    """
    brain.screen.print("Driver Control")

    while True:
        # --- ARCADE DRIVE CONTROL ---
        # Axis3 = Forward/Backward
        # Axis1 = Turning Left/Right
        
        axis3_pos = controller_1.axis3.position()
        axis1_pos = controller_1.axis1.position()

        # Apply Deadzone Logic
        if abs(axis3_pos) < DEADZONE:
            axis3_pos = 0
        if abs(axis1_pos) < DEADZONE:
            axis1_pos = 0

        # Calculate motor speeds
        left_speed = axis3_pos + axis1_pos
        right_speed = axis3_pos - axis1_pos

        # Spin motors
        left_drive_group.spin(FORWARD, left_speed, PERCENT)
        right_drive_group.spin(FORWARD, right_speed, PERCENT)

        # --- MECHANISM CONTROLS ---
        
        # Intake Control (L1 to spin, L2 to stop/reverse)
        if controller_1.buttonL1.pressing():
            intake_motor.spin(FORWARD, INTAKE_SPEED, PERCENT)
        elif controller_1.buttonL2.pressing():
            intake_motor.spin(REVERSE, INTAKE_SPEED, PERCENT)
        else:
            intake_motor.stop() # or set to hold if needed

        # --- SYSTEM PAUSE ---
        # CRITICAL: Must have a wait to prevent the Brain from freezing
        wait(20, MSEC)

# =============================================================================
# 5. MAIN EXECUTION
# =============================================================================

# Create the competition object
comp = Competition(user_control, autonomous)

# Run the pre-autonomous function
pre_autonomous()