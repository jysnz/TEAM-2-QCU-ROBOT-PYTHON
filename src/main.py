# ---------------------------------------------------------------------------- #
#   Module:       main.py                                                      #
#   Description:  VEX V5 Competition Template with Input Scaling               #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math  # Imported for math functions if needed later

# =============================================================================
# 1. ROBOT CONFIGURATION
# =============================================================================

# Brain and Controller
brain = Brain()
controller_1 = Controller()

# Motors
left_front = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_back  = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_front = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
right_back  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
arm_motor = Motor(Ports.PORT8, GearSetting.RATIO_36_1, False)

# Motor Groups
left_drive_group = MotorGroup(left_front, left_back)
right_drive_group = MotorGroup(right_front, right_back)

# Sensors
inertial = Inertial(Ports.PORT15)

# =============================================================================
# 2. GLOBAL CONSTANTS & VARIABLES
# =============================================================================

DRIVE_SPEED = 80
TURN_SPEED = 50
INTAKE_SPEED = 100
DEADZONE = 5

# =============================================================================
# 3. HELPER FUNCTIONS
# =============================================================================

def scale_input(value):
    """
    Converts a linear input (-100 to 100) to a cubic curve.
    Formula: (Input^3) / 10000
    Example: Input 50 -> Output 12.5 (Precise)
    Example: Input 100 -> Output 100 (Fast)
    """
    # Calculate cubic value
    # We divide by 10000 because 100^3 is 1,000,000, but we want max result to be 100.
    return (value ** 3) / 10000

def move_arm_to(target_angle, speed):
    arm_motor.set_stopping(HOLD)
    arm_motor.spin_to_position(target_angle, DEGREES, speed, PERCENT, wait=False)

def turn_right(degrees, speed):
    left_drive_group.set_velocity(speed, PERCENT)
    right_drive_group.set_velocity(speed, PERCENT)
    left_drive_group.spin_for(FORWARD, degrees, DEGREES, wait=False)
    right_drive_group.spin_for(REVERSE, degrees, DEGREES, wait=True)

# =============================================================================
# 4. COMPETITION FUNCTIONS
# =============================================================================

def pre_autonomous():
    brain.screen.print("Calibrating Inertial...")
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("System Ready!")
    
    arm_motor.reset_position()
    left_drive_group.reset_position()
    right_drive_group.reset_position()

def autonomous():
    brain.screen.print("Running Autonomous")
    wait(200, MSEC)
    turn_right(90, TURN_SPEED)

def user_control():
    brain.screen.print("Driver Control")

    while True:
        # --- INPUTS ---
        # Get raw values from controller
        raw_forward = controller_1.axis3.position()
        raw_turn = controller_1.axis1.position()

        # --- DEADZONE LOGIC ---
        if abs(raw_forward) < DEADZONE:
            raw_forward = 0
        if abs(raw_turn) < DEADZONE:
            raw_turn = 0

        # --- INPUT SCALING (THE NEW PART) ---
        # Apply the cubic math to the raw inputs
        forward_input = scale_input(raw_forward)
        turn_input = scale_input(raw_turn)

        # --- MIXING SPEEDS ---
        left_speed = forward_input + turn_input
        right_speed = forward_input - turn_input

        # --- MOTOR OUTPUT ---
        left_drive_group.spin(FORWARD, left_speed, PERCENT)
        right_drive_group.spin(FORWARD, right_speed, PERCENT)

        # --- MECHANISM CONTROLS ---
        if controller_1.buttonR1.pressing():
            move_arm_to(120, 80)
        elif controller_1.buttonR2.pressing():
            move_arm_to(0, 40)

        # --- SYSTEM PAUSE ---
        # Only need one wait at the end of the loop
        wait(20, MSEC)

# =============================================================================
# 5. MAIN EXECUTION
# =============================================================================

comp = Competition(user_control, autonomous)
pre_autonomous()