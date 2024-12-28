from pybricks.ev3devices import GyroSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.parameters import Port, Direction
from pybricks.tools import wait
#from movement import turn


# Set positive direction as clockwise (default)
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=150)


def turn(angle):
    robot.turn(angle*2)

# Reset the angle of the gyroscope to 90 at the start
def reset_angle(graus, gyro_sensor):
    gyro_sensor.reset_angle(graus)

# Function to turn the robot by a specified angle

#target_angle tem valores entre ]-180, 180]
def adjust_angle(target_angle, gyro_sensor):
    reset_angle(gyro_sensor.angle() % 360, gyro_sensor)

    if(gyro_sensor.angle() < -180):
        gyro_sensor.reset_angle(360 + gyro_sensor.angle())
    elif(gyro_sensor.angle() > 180):
        gyro_sensor.reset_angle(-360 + gyro_sensor.angle())

    if(gyro_sensor.angle() < 0 and target_angle == 180):
        target_angle = -180


    angulo = target_angle - gyro_sensor.angle()
 
    print("angulo: ", angulo)
    
    if(angulo>0):
        #target_angle = target_angle * 2

            print("Vira COUNTER-CLOCKWISE")
            print("targetAngle: ", target_angle)
            print("angulo atual acumulado: ", gyro_sensor.angle())


            turn(angulo)
            angulo = target_angle - gyro_sensor.angle()

            print("angulo: ", angulo)


            
    else:
        #while(angulo < 0):


        print("Vira CLOCKWISE")
        print("targetAngle: ", target_angle)
        print("angulo atual acumulado: ", gyro_sensor.angle())


        turn(angulo)
        angulo = target_angle - gyro_sensor.angle()
            
        print("angulo: ", angulo)

     
    print("Angle after reset: ", gyro_sensor.angle())