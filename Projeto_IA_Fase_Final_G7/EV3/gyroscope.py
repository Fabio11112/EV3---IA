from pybricks.ev3devices import GyroSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.parameters import Port, Direction
from pybricks.tools import wait


# Set positive direction as clockwise (default)
left_motor = Motor(Port.C)
right_motor = Motor(Port.D)
wheel_diameter=55.5
axle_track=150
print("Wheel Diameter:", wheel_diameter)
print("Axle Track:", axle_track)    


robot = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)


def turn(angle):
    """Gira o robô em um ângulo específico.
        Args:
            angle (int): O ângulo em graus para girar. 
            Um valor positivo gira no sentido horário e um valor negativo gira no sentido anti
            horário.   
    """
    robot.turn(angle*2)

# Reset the angle of the gyroscope to 90 at the start
def reset_angle(graus, gyro_sensor):
    """Reseta o ângulo do sensor giroscópio para um valor específico.
        Args:
            angle (int): O ângulo em graus para resetar.
            Um valor positivo gira no sentido horário e um valor negativo gira no sentido anti
            horário.
            gyro_sensor (GyroSensor): O sensor giroscópio que será resetado.
    """
    gyro_sensor.reset_angle(graus)

# Function to turn the robot by a specified angle

#target_angle tem valores entre ]-180, 180]
def adjust_angle(target_angle, gyro_sensor):
    """
    Ajusta o ângulo do robô para um valor específico.
        Args:
            target_angle (int): O ângulo em graus para ajustar.
            Um valor positivo gira no sentido horário e um valor negativo gira no sentido anti
            horário.
            gyro_sensor (GyroSensor): O sensor giroscópio que será resetado.
    """
    reset_angle(gyro_sensor.angle() % 360, gyro_sensor)

    if(gyro_sensor.angle() < -180):
        gyro_sensor.reset_angle(360 + gyro_sensor.angle())
    elif(gyro_sensor.angle() > 180):
        gyro_sensor.reset_angle(-360 + gyro_sensor.angle())

    if(gyro_sensor.angle() < 0 and target_angle == 180):
        target_angle = -180
    angulo = target_angle - gyro_sensor.angle()
    print("diferença de ângulos: ", angulo)
    if(angulo>0):
            print("Vira COUNTER-CLOCKWISE")
            print("targetAngle: ", target_angle)
            print("angulo atual acumulado: ", gyro_sensor.angle())
            turn(angulo)
            angulo = target_angle - gyro_sensor.angle()
            
    else:    
        print("Vira CLOCKWISE")
        print("targetAngle: ", target_angle)
        print("angulo atual acumulado: ", gyro_sensor.angle())
        turn(angulo)
        angulo = target_angle - gyro_sensor.angle()
        print("angulo: ", angulo)

     
    #print("Angle after reset: ", gyro_sensor.angle())