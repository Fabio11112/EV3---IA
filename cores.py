# Importar as bibliotecas necessárias do Pybricks
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.hubs import EV3Brick
from pybricks.tools import wait

# Inicializar o hub EV3
ev3 = EV3Brick()
# Inicializar o sensor de cor na porta 1 (ajustar se estiver conectado a outra porta)
#sensor_de_cor = ColorSensor(Port.S3)

# Definir intervalos de cores em RGB (min, max) para cada componente RGB
cores_intervalos = {
    "Laranja": ((70, 80), (20, 30), (10, 15)),
    "Laranja claro": ((75, 80), (30, 40), (10, 20)),
    "Amarelo Escuro": ((75, 80), (45, 55), (15, 20)),
    "Amarelo": ((75, 80), (55, 65), (15, 20)),
    "Verde": ((20, 30), (55, 65), (15, 20)),
    "Verde Escuro": ((10, 20), (30, 40), (20, 30)),
    "Azul": ((10, 25), (35, 50), (55, 70)),
    "Azul escuro": ((10, 15), (20, 30), (50, 55)),
    "Roxo": ((20, 30), (10, 20), (30, 40)),
    "Cor de rosa": ((50, 60), (10, 15), (20, 25)),
    "Cor de rosa claro": ((65, 75), (10, 20), (15, 25)),
    "Vermelho": ((65, 75), (10, 20), (10, 15)),
    "Branco": ((75, 85),(85, 95),(95, 105)),
    "Preto": ((0, 10), (0, 10), (0, 10))
} 

# Função para verificar se o RGB está dentro do intervalo especificado
def cor_dentro_do_intervalo(r, g, b, intervalo):
    (r_min, r_max), (g_min, g_max), (b_min, b_max) = intervalo
    return r_min <= r <= r_max and g_min <= g <= g_max and b_min <= b <= b_max

# Função para detectar a cor com base nos intervalos de cores
def detectar_cor_por_intervalo(r, g, b):
    for cor, intervalo in cores_intervalos.items():
        if cor_dentro_do_intervalo(r, g, b, intervalo):
            return cor
    return "Cor desconhecida"


# wait(2000)
