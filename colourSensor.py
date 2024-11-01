from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.parameters import Color

sensor_de_cor = ColorSensor(Port.S2)
# 0 = Sem cor, 1 = Preto, 2 = Azul, 3 = Verde, 4 = Amarelo, 5 = Vermelho, 6 = Branco, 7 = Castanho2
def detectar_cor():
    #cor_detectada_rgb = sensor_de_cor.color()  # Ler a cor detectada
    cor_detectada = sensor_de_cor.rgb()
    cor_nome = sensor_de_cor.color()
    # Também é possível ler a intensidade da luz refletida
    intensidade_luz_refletida = sensor_de_cor.reflection()
    
    return (cor_detectada, cor_nome)