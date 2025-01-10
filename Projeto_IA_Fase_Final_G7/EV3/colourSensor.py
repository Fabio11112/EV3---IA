from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.parameters import Color
from pybricks.tools import wait
from pybricks.hubs import EV3Brick
import json

JSON_file = "cores.json"
ev3 = EV3Brick()

sensor_de_cor = ColorSensor(Port.S2)

def detectar_cor():
    """método que deteta a cor do sensor de cor

    Returns:
        tuplo: retorna a cor detectada e o nome da cor
    """
    cor_detectada = sensor_de_cor.rgb()
    cor_nome = sensor_de_cor.color()
    # Também é possível ler a intensidade da luz refletida
    intensidade_luz_refletida = sensor_de_cor.reflection()
    return (cor_detectada, cor_nome)

def pre_configuracao():
    """método que faz a leitura de 4 cores distintas, azul, vermelho, preto e branco, e as retorna
    num dicionário para futura configuração

    Returns:
        Dicionário: dicionário com os valores rgb de cada cor guardada
    """
    azul = sensor_de_cor.rgb()
    print("azul: ", azul)
    ev3.speaker.beep(400,200)
    wait(2000)
    vermelho = sensor_de_cor.rgb()
    print("vermelho: ", vermelho)
    ev3.speaker.beep(400,200)
    wait(2000)
    preto = sensor_de_cor.rgb()
    print("preto: ", preto)
    ev3.speaker.beep(400,200)
    wait(2000)
    branco = sensor_de_cor.rgb()
    print("branco: ", branco)
    ev3.speaker.beep(400,200)
    return {"Azul":azul, "Vermelho":vermelho, "Preto":preto, "Branco":branco}

def guardar_configuracao_cores():
    """método que guarada a configuração das cores num ficheiro JSON
    """
    cores = pre_configuracao()
    with open(JSON_file, 'w') as f:
        json.dump(cores, f, indent=4)