from libraries import UltrasonicSensor, Port, wait

def sensorUltrasonic(ev3):
    """
    Função que retorna a distância do sensor ultrassônico
    Args:
        ev3: objeto da classe EV3
    Returns:
        distance: distância em cm
    """
    ultrasonic_sensor = UltrasonicSensor(Port.S3)
    distance = ultrasonic_sensor.distance()
    return distance
