import numpy as np


def promediar_puntos_cercanos(contornos, umbral_distancia=5):
    contornos_simplificados = []

    for contorno in contornos:
        if len(contorno) > 1:
            puntos_promediados = [contorno[0]]  # Iniciar con el primer punto
            for i in range(1, len(contorno)):
                distancia = np.linalg.norm(contorno[i] - puntos_promediados[-1])
                if distancia < umbral_distancia:
                    # Promediar el punto actual con el anterior
                    punto_promedio = (contorno[i] + puntos_promediados[-1]) / 2
                    puntos_promediados[-1] = punto_promedio
                else:
                    puntos_promediados.append(contorno[i])
            contornos_simplificados.append(np.array(puntos_promediados, dtype=np.int32))
        else:
            contornos_simplificados.append(contorno)

    return contornos_simplificados
