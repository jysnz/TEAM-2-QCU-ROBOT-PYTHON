# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       [Your Name]                                                  #
#   Created:      [Date]                                                       #
#   Description:  VEX V5 Competition Template (Updated with Safety Break)      #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# =============================================================================
# 1. ROBOT CONFIGURATION
# =============================================================================

# Brain and Controller
brain = Brain()
controller_1 = Controller()

# Motors (Drivetrain)
left_front = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
left_middle = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
left_back  = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_front = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
right_middle = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
right_back  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

left_drive_group = MotorGroup(left_front, left_middle, left_back)
right_drive_group = MotorGroup(right_front, right_middle, right_back)

# Mechanism Motors
intake_motor = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
match_loader = Motor(Ports.PORT4, GearSetting.RATIO_6_1, False)

# --- UPDATED: CATAPULT MOTOR (Now 0-45 degrees) ---
catapult_motor = Motor(Ports.PORT6, GearSetting.RATIO_36_1, False)
catapult_motor.set_stopping(HOLD)
catapult_motor.set_velocity(60, PERCENT) 
catapult_motor.reset_position() 

# --- NEW: CATAPULT ARM (0-125 degrees) ---
# Assuming Port 7 is free. Change this if needed.
catapult_arm = Motor(Ports.PORT7, GearSetting.RATIO_36_1, False)
catapult_arm.set_stopping(HOLD) # Holds position when stopped
catapult_arm.set_velocity(50, PERCENT)
catapult_arm.reset_position()



# Sensors
inertial = Inertial(Ports.PORT15)

# =============================================================================
# 2. GLOBAL CONSTANTS & VARIABLES
# =============================================================================

# Speed Settings
DRIVE_SPEED = 80
TURN_SPEED = 50
INTAKE_SPEED = 100
CATAPULT_SPEED = 60 
MATCHLOADER_SPEED = 50

# Deadzone
DEADZONE = 5

# --- STATE VARIABLES ---
# Catapult (Small) Variables
catapult_is_up = False      
r1_was_pressed = False 

# Arm (Big) Variables
arm_is_up = False
r2_was_pressed = False

# =============================================================================
# 3. HELPER FUNCTIONS
# =============================================================================

def drive_forward(distance_cm, speed, MM):
    """Moves the robot forward for a set distance."""
    left_drive_group.set_velocity(speed, PERCENT)
    right_drive_group.set_velocity(speed, PERCENT)
    left_drive_group.spin_for(FORWARD, distance_cm, MM, wait=False)
    right_drive_group.spin_for(FORWARD, distance_cm, MM, wait=True)

def turn_right(degrees, speed):
    """Turns the robot right."""
    left_drive_group.set_velocity(speed, PERCENT)
    right_drive_group.set_velocity(speed, PERCENT)
    left_drive_group.spin_for(FORWARD, degrees, DEGREES, wait=False)
    right_drive_group.spin_for(REVERSE, degrees, DEGREES, wait=True)

# --- NEW: SAFETY BREAK FUNCTION ---
def move_motor_safely(motor_obj, target_degrees, speed):
    """
    Moves a motor to a position, but stops immediately (BREAK)
    if the motor stops moving (hits a part) before reaching the target.
    """
    # 1. Start moving the motor (Non-blocking)
    motor_obj.spin_to_position(target_degrees, DEGREES, speed, PERCENT, wait=False)
    
    # 2. Wait a tiny bit to let the motor start moving so we don't detect false stop
    wait(200, MSEC)

    # 3. Monitor the motor while it is supposed to be spinning
    while motor_obj.is_spinning():
        
        # Check current velocity
        current_velocity = motor_obj.velocity(PERCENT)
        
        # If velocity is less than 2% (stalled/hit something)
        if abs(current_velocity) < 2:
            # FORCE STOP / BRAKE
            motor_obj.stop(BRAKE)
            brain.screen.print("OBSTRUCTION DETECTED!")
            break # Exit the loop
            
        wait(20, MSEC)

# =============================================================================
# 4. COMPETITION FUNCTIONS
# =============================================================================

def pre_autonomous():
    brain.screen.print("Calibrating Inertial...")
    inertial.calibrate()
    while inertial.is_calibrating():
        wait(100, MSEC)
        
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("System Ready!")
    
    left_drive_group.reset_position()
    right_drive_group.reset_position()
    
    catapult_motor.reset_position()
    catapult_arm.reset_position()

def autonomous():
    brain.screen.print("Running Autonomous")
    # Example: Move the new arm safely
    move_motor_safely(catapult_arm, 125, 50)

def user_control():
    global catapult_is_up, r1_was_pressed, matchloader_on
    global arm_is_up, r2_was_pressed
    
    brain.screen.print("Driver Control")

    while True:
        # --- DRIVETRAIN (Arcade) ---
        axis3_pos = controller_1.axis3.position()
        axis1_pos = controller_1.axis1.position()

        if abs(axis3_pos) < DEADZONE: axis3_pos = 0
        if abs(axis1_pos) < DEADZONE: axis1_pos = 0

        left_speed = -axis3_pos + axis1_pos
        right_speed = -axis3_pos - axis1_pos

        left_drive_group.spin(FORWARD, left_speed, PERCENT)
        right_drive_group.spin(FORWARD, right_speed, PERCENT)

        # --- OUTTAKE (L2/R2) ---
        if controller_1.buttonL2.pressing() and controller_1.buttonR2.pressing():
            intake_motor.spin(REVERSE, INTAKE_SPEED, PERCENT)
        else:
            intake_motor.stop()

        # --- INTAKE (L1/R1) ---
        if controller_1.buttonL1.pressing() and controller_1.buttonR1.pressing():
            intake_motor.spin(FORWARD, INTAKE_SPEED, PERCENT)
        else:
            intake_motor.stop()
        
        #Matchload
        if controller_1.buttonB.pressing():
            move_motor_safely(match_loader, -75, MATCHLOADER_SPEED)
            match_loader.stop(BRAKE)
        else:
            match_loader.stop()

        if controller_1.buttonDown.pressing():
            left_speed = axis3_pos + axis1_pos
            right_speed = axis3_pos - axis1_pos
        else:
            left_speed = -axis3_pos + axis1_pos
            right_speed = -axis3_pos - axis1_pos
            
        # --- UPDATED: ORIGINAL CATAPULT (R1) -> Goes 0 to 45 ---
        if controller_1.buttonR1.pressing():
            if not r1_was_pressed: 
                if catapult_is_up:
                    # Go down to 0
                    move_motor_safely(catapult_motor, 0, CATAPULT_SPEED)
                    catapult_is_up = False
                else:
                    # Go up to 45 (Updated Range)
                    move_motor_safely(catapult_motor, 45, CATAPULT_SPEED)
                    catapult_is_up = True
                r1_was_pressed = True
        else:
            r1_was_pressed = False

        # --- NEW: CATAPULT ARM (R2) -> Goes 0 to 125 ---
        if controller_1.buttonR2.pressing():
            if not r2_was_pressed: 
                if arm_is_up:
                    # Go down to 0
                    move_motor_safely(catapult_arm, 0, 50)
                    arm_is_up = False
                else:
                    # Go up to 125
                    move_motor_safely(catapult_arm, 125, 50)
                    arm_is_up = True
                r2_was_pressed = True
        else:
            r2_was_pressed = False

        wait(20, MSEC)

# =============================================================================
# 5. MAIN EXECUTION
# =============================================================================

comp = Competition(user_control, autonomous)
pre_autonomous()