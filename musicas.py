
#from libraries import *
from pybricks.tools import wait
from pybricks.hubs import EV3Brick
QUARTER_NOTE = 200  # Nota negra rápida
EIGHTH_NOTE = 100   # Nota corchea rápida
SIXTEENTH_NOTE = 50 # Nota semicorchea rápida

ev3 = EV3Brick()

def imperialMarch(ev3):
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





def batman_melody(ev3):

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



def spooky_scary():
    A3= 220
    Bb3= 233
    B3= 247
    C4= 262
    Db4= 277
    D4= 294
    Eb4= 311
    E4= 330
    F4= 349
    Gb4= 370
    G4= 392
    Ab4= 415
    A4= 440
    Bb4= 466
    B4= 494
    C5= 523
    Db5= 554
    D5= 587
    Eb5= 622
    E5= 659
    F5= 698
    Gb5= 740 



    ev3.speaker.beep(G4, QUARTER_NOTE)  # Spooky
    wait(QUARTER_NOTE)
    ev3.speaker.beep(G4, EIGHTH_NOTE)   # Sca-
    wait(EIGHTH_NOTE)
    ev3.speaker.beep(Gb4, EIGHTH_NOTE)   # ry
    wait(EIGHTH_NOTE)
    ev3.speaker.beep(Gb4, QUARTER_NOTE)  # Ske-
    wait(QUARTER_NOTE)
    ev3.speaker.beep(B3, EIGHTH_NOTE)   # le-
    wait(EIGHTH_NOTE)
    ev3.speaker.beep(D4, EIGHTH_NOTE)   # tons
    wait(EIGHTH_NOTE)
    ev3.speaker.beep(B3, QUARTER_NOTE)  # Send
    wait(QUARTER_NOTE)
    wait(QUARTER_NOTE)
    ev3.speaker.beep(B3, EIGHTH_NOTE)   # shiv-
    wait(EIGHTH_NOTE)
    ev3.speaker.beep(B3, EIGHTH_NOTE)   # ers
    wait(EIGHTH_NOTE)
    ev3.speaker.beep(G4, QUARTER_NOTE)  # down
    wait(QUARTER_NOTE)
    ev3.speaker.beep(G4, EIGHTH_NOTE)   # your
    wait(EIGHTH_NOTE)
    ev3.speaker.beep(Gb4, EIGHTH_NOTE)   # spine
    wait(QUARTER_NOTE)
    ev3.speaker.beep(Gb4, EIGHTH_NOTE)   # spine
    wait(QUARTER_NOTE)
    ev3.speaker.beep(B3, EIGHTH_NOTE)   # spine
    
    wait(QUARTER_NOTE)