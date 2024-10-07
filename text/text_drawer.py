import time
from segments import segment_map, vertices
from cobot.rodri import init
import numpy as np

z_high = 0.08
z_low = 0.062

# Velocidad fija predeterminada (en unidades por segundo)
FIXED_VELOCITY = 0.25  # Ajusta esta velocidad según sea necesario
# Aceleración arbitraria (en unidades por segundo cuadrado)
ARBITRARY_ACCELERATION = 0.1  # Ajusta esta aceleración según sea necesario


class TextDrawer:
    @staticmethod
    def draw_text(text):
        print("DRAWING TEXT")
        letters = list(text)

        s = init()

        inital_pos = (0.7, 0.3, z_high)
        send_command(s, inital_pos[0], inital_pos[1], z_high)
        time.sleep(1)
        current_pos = (0.7, 0.3, z_high)
        row = 1
        column = 1
        #draw letter
        for letter in letters:
            if column == 8:
                row += 1
                if row < 5:
                    column = 1
                    distance = calculate_distance(inital_pos[0], inital_pos[1], inital_pos[0] - 0.15, 0.3)
                    time_to_travel = calculate_time(distance, FIXED_VELOCITY)
                    time_to_travel = time_to_travel if time_to_travel > 0.6 else 0.6
                    inital_pos = (inital_pos[0] - 0.12, 0.3, z_high)

                    send_command(s, inital_pos[0], inital_pos[1], inital_pos[2], time_to_travel)
                    time.sleep(time_to_travel)
                else:
                    break
            column += 1

            if letter == ' ':
                inital_pos = (inital_pos[0], inital_pos[1] - 0.1, z_high)
                continue
            letter = letter.upper()
            send_command(s, inital_pos[0], inital_pos[1], inital_pos[2])
            # position = draw(s, position, inital_pos[0], inital_pos[1], inital_pos[2])
            arr = segment_map.get(letter)

            for i in range(len(arr)):
                value = arr[i]
                points = vertices.get(i + 1)
                current_pos = (inital_pos[0] + points[0][0], inital_pos[1] + points[0][1])
                if value == 1:
                    if  i == 0 or (i > 0 and (arr[i - 1] == 0)):
                        print('sube')
                        send_command(s, current_pos[0], current_pos[1], z_high)
                        # position = draw(s, position, current_pos[0], current_pos[1], z_high)
                        time.sleep(2)

                    send_command(s, current_pos[0], current_pos[1], z_low)
                    # position = draw(s, position, current_pos[0], current_pos[1], z_low)
                    if i == 0 or (i > 0 and (arr[i - 1] == 0)):
                        time.sleep(2)
                    else:
                        time.sleep(1)
                    current_pos = (inital_pos[0] + points[1][0], inital_pos[1] + points[1][1])
                    print(current_pos)

                    send_command(s, inital_pos[0] + points[1][0], inital_pos[1] + points[1][1], z_low)
                    # position = draw(s, position, inital_pos[0] + points[1][0], inital_pos[1] + points[1][1], z_low)
                    time.sleep(1)
                    if i + 1 < len(arr) and (arr[i + 1] == 0):
                        send_command(s, inital_pos[0] + points[1][0], inital_pos[1] + points[1][1], z_high)
                        # position = draw(s, position, inital_pos[0] + points[1][0], inital_pos[1] + points[1][1], z_high)
                        time.sleep(1)

            inital_pos = (inital_pos[0], inital_pos[1] - 0.1, z_high)

        send_command(s, current_pos[0], current_pos[1], z_high)
        # position = draw(s, position, current_pos[0], current_pos[1], z_high)
        time.sleep(3)
        send_command(s, 0.7, 0.3, z_high)
        # draw(s, position, 0.7, 0.3, z_high)

def draw(s, position, x2, y2, z):
    distance = calculate_distance(position[0],position[1], x2, y2)
    time_to_travel = calculate_time(distance, 0.05)
    time_to_travel = time_to_travel if time_to_travel > 0.6 else 0.6
    send_command(s, position[0],position[1], z, time_to_travel)
    time.sleep(time_to_travel)
    return (x2, y2, z)


# Calcula la distancia entre dos puntos
def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Calcula el tiempo necesario para moverse entre dos puntos dado una velocidad fija
def calculate_time(distance, velocity):
    return distance / velocity

def send_command(s, x, y, z, t=None):
    if t is None:
        # Enviar comando con velocidad fija y aceleración arbitraria
        command = f"movel(p[{x:.2f}, {y:.2f}, {z:.2f}, 2.5, -1.9, 0], a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f})\n"
    else:
        # Enviar comando con velocidad fija y aceleración arbitraria
        command = f"movel(p[{x:.2f}, {y:.2f}, {z:.2f}, 2.5, -1.9, 0], a={ARBITRARY_ACCELERATION:.2f}, v={FIXED_VELOCITY:.2f}, t={t:.2f})\n"
    s.send(command.encode('utf-8'))
    print(f"Command sent: {command}")

