
from vex import *

brain = Brain()
controller_1 = Controller(PRIMARY)

left_motor_f = Motor(Ports.PORT1,GearSetting.RATIO_18_1,True)
left_motor_b = Motor(Ports.PORT5,GearSetting.RATIO_18_1,True)
left_drive_smart = MotorGroup(left_motor_f,left_motor_b)
right_motor_f = Motor(Ports.PORT3, GearSetting.RATIO_18_1,False)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1,False)
right_drive_smart = MotorGroup(right_motor_f,right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 317.5, 300, MM, 0.2857142857142857)

motor6= Motor(Ports.PORT6,GearSetting.RATIO_18_1,True)# top long goal
motor7 = Motor(Ports.PORT7,GearSetting.RATIO_18_1,True)# inside middle
motor8 = Motor(Ports.PORT8,GearSetting.RATIO_18_1,True)#middle goal
# motor10 = Motor(Ports.PORT10,GearSetting.RATIO_18_1,False)
motor20 = Motor(Ports.PORT20,GearSetting.RATIO_18_1,True)#basket
motor19 = Motor(Ports.PORT19,GearSetting.RATIO_18_1,True)# arm 


arm = False


motor19.set_max_torque(50, PERCENT)
def toggle_arm():
    global arm

    if arm:

        motor19.spin(FORWARD,100,PERCENT)
        at_max(motor19,lambda:motor19.stop)
        motor19.set_stopping(HOLD)
        arm = False
        print("False")
    else:
  
        motor19.spin(REVERSE,100,PERCENT)
        at_max(motor19,lambda:motor19.stop)
        motor19.set_stopping(HOLD)
        arm = True
        print("True")




def at_max(motor:Motor,callback):

    wait(200,MSEC)



    while not motor.is_spinning():
       
        if not abs(motor.velocity()) > 0:
            print("maxed")
            callback()  
            break
        wait(10,MSEC)


def drivetrain_movement():
    forward = controller_1.axis3.position()
    turn = controller_1.axis1.position()

    left_speed = (forward - turn) *2
    right_speed = (forward + turn) * 2
    left_drive_smart.spin(FORWARD,left_speed,PERCENT)
    right_drive_smart.spin(FORWARD,right_speed,PERCENT)
    return
def pre_autonomous():

    return

def autonomous():
    



    return
def drivers_control():
   
    controller_1.buttonDown.pressed(toggle_arm)
    while True:
        drivetrain_movement()
        if controller_1.buttonB.pressing():#intake
            motor7.spin(FORWARD, 100,PERCENT)
            motor8.spin(FORWARD,100,PERCENT)
            motor20.spin(REVERSE,100,PERCENT)
        elif controller_1.buttonL2.pressing():#outtake
            motor8.spin(REVERSE, 100,PERCENT)
            motor7.spin(REVERSE,100,PERCENT)
            motor20.spin(FORWARD,100,PERCENT)
        elif controller_1.buttonR1.pressing():#middle
            motor6.spin(REVERSE,100,PERCENT)
            motor7.spin(REVERSE,100,PERCENT)
            motor8.spin(FORWARD,100,PERCENT)
            motor20.spin(FORWARD,100,PERCENT)
        elif controller_1.buttonR2.pressing():#long_goal
            motor6.spin(FORWARD,100,PERCENT)
            motor7.spin(REVERSE,100,PERCENT)
            motor8.spin(FORWARD,100,PERCENT)
            motor20.spin(FORWARD,100,PERCENT)
            
        

            
        else:
            motor20.stop()
            motor6.stop()
            motor7.stop()
            motor8.stop()
                
comp = Competition(drivers_control,autonomous)
# comp = Competition(autonomous,drivers_control)

pre_autonomous()
