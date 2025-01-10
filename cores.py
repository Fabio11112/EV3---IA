# Importar as bibliotecas necessárias do Pybricks
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Port
from pybricks.hubs import EV3Brick
from pybricks.tools import wait
from colourSensor import pre_configuracao
import json

JSON_file = "cores.json"

# Inicializar o hub EV3
ev3 = EV3Brick()
# Inicializar o sensor de cor na porta 1 (ajustar se estiver conectado a outra porta)

#array de cores e respetivos intervalos de rgb
cores_intervalos = {}

def pre_configuracao_cores():
    """método que carrega a pré configuração das cores
    """
    r, g, b = 0, 1, 2 
    cores = carregar_configuracao_cores(JSON_file)
    for i in cores.keys():
        cores_intervalos[i] = (cores[i][r]-20, cores[i][r]+20), (cores[i][g]-20, cores[i][g]+20), (cores[i][b]-20, cores[i][b]+20)



# Função para verificar se o RGB está dentro do intervalo especificado
def cor_dentro_do_intervalo(r, g, b, intervalo):
    """método que verifica se a cor está dentro do intervalo especificado

    Args:
        r (number): componente r do rgb
        g (number): componente g do rgb
        b (number): componente b do rgb
        intervalo (tuplo): intervalos de cada componente do rgb

    Returns:
        booleano: True se a cor estiver no intervalo, False caso contrário
    """
    (r_min, r_max), (g_min, g_max), (b_min, b_max) = intervalo
    return r_min <= r <= r_max and g_min <= g <= g_max and b_min <= b <= b_max

# Função para detectar a cor com base nos intervalos de cores
def detectar_cor_por_intervalo(r, g, b):
    """método que deteta a cor com base nos intervalos de cores

    Args:
        r (number): componente r do rgb
        g (number): componente g do rgb
        b (number): componente b do rgb

    Returns:
        String: nome da cor detetada
    """
    for cor, intervalo in cores_intervalos.items():
        if cor_dentro_do_intervalo(r, g, b, intervalo):
            print(cor)
            return cor
    return "Cor desconhecida"

def carregar_configuracao_cores(filename):
    """método que devolve o JSON da pré-configuração

    Args:
        filename (String): nome do ficheiro JSON

    Returns:
        Dicionário: objeto JSON com a configuração das cores
    """
    with open(filename, 'r') as json_file:
        configuracao_cores = json.load(json_file)
    return configuracao_cores


# Executar a pré-configuração das cores
pre_configuracao_cores()