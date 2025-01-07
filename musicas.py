
#from libraries import *
from pybricks.tools import wait
from pybricks.hubs import EV3Brick
QUARTER_NOTE = 200  # Nota negra rápida
EIGHTH_NOTE = 100   # Nota corchea rápida
SIXTEENTH_NOTE = 50 # Nota semicorchea rápida

ev3 = EV3Brick()

def tocar_musica_vitoria():
    # Sequência de notas para a musiquinha de vitória
    victory_melody = [
        (523, 300),  # C5
        (659, 300),  # E5
        (784, 300),  # G5
        (1047, 600), # C6
        (784, 300),  # G5
        (1047, 300), # C6
        (1319, 600), # E6
    ]
    # Toca as notas
    tocar_musica(ev3, victory_melody)

def tocar_musica_derrota():
# Notas e durações da música de Game Over do Super Mario Bros (frequências em Hz e duração em ms)
    melody = [
        (659, 300),  # E5
        (622, 300),  # D#5
        (659, 300),  # E5
        (622, 300),  # D#5
        (659, 300),  # E5
        (494, 600),  # B4
        (587, 300),  # D5
        (523, 300),  # C5
        (440, 900),  # A4
    ]
    tocar_musica(ev3, melody)

# Método para reproduzir a música
def tocar_musica(ev3, musica):
    for nota, duracao in musica:
        if nota == 0:
            wait(duracao)  # Pausa
        else:
            ev3.speaker.beep(frequency=nota, duration=duracao)
        wait(50)  # Pausa curta entre as notas

# Toca a música de Game Over



def imperialMarch():
# Define the notes (in Hz) and durations (in ms) for the Imperial March
    imperial_march = [
        (440, 500),  # A4
        (440, 500),  # A4
        (440, 500),  # A4
        (349, 350),  # F4
        (523, 150),  # C5
        (440, 500),  # A4
        (349, 350),  # F4
        (523, 150),  # C5
        (440, 1000), # A4
        (659, 500),  # E5
        (659, 500),  # E5
        (659, 500),  # E5
        (698, 350),  # F5
        (523, 150),  # C5
        (415, 500),  # G#4
        (349, 350),  # F4
        (523, 150),  # C5
        (440, 1000)  # A4
    ]

    # Play each note in the sequence
    for freq, duration in imperial_march:
        ev3.speaker.beep(freq, duration)
        wait(duration/2)





def batman_melody():

    # Definimos las frecuencias de las notas (en Hz)
    G4 = 392  # G4: La nota "sol" en la cuarta octava
    C5 = 523  # C5: La nota "do" en la quinta octava

    # Definimos la duración de las notas (en milisegundos)
    NA_DURATION = 150  # Duración de cada "Na"
    BATMAN_DURATION = 500  # Duración del "Batman"
    # Tocar las "Na na na na na na na na"
    for _ in range(8):
        ev3.speaker.beep(G4, NA_DURATION)
        wait(NA_DURATION)
    
    # Tocar "Batman!"
    ev3.speaker.beep(C5, BATMAN_DURATION)
    wait(BATMAN_DURATION)


 