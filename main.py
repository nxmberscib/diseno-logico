import math
import time

# Alfabeto personalizado de 64 símbolos (10 + 27 + 27)
DIGITOS = "0123456789"
MAYUSCULAS = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
MINUSCULAS = "abcdefghijklmnñopqrstuvwxyz"

ALFABETO = DIGITOS + MAYUSCULAS + MINUSCULAS


def calcular_r_minimo(C, N):
    """Calcula la cantidad mínima de dígitos R requeridos usando enteros."""
    if C == 0:
        return 1
    r = 0
    capacidad = 1
    while capacidad <= C:
        capacidad *= N
        r += 1
    return r


def contar_y_convertir():
    while True:
        print("\n=== SISTEMA DE CONTEO UNIVERSAL ===")

        try:
            R = int(input("Ingrese R (Cantidad inicial de dígitos): "))
            C = int(input("Ingrese C (Número total de conteos): "))
            N = int(input("Ingrese N (Base para el conteo, 2-64): "))
            B = int(input("Ingrese B (Base a la cual convertir al final, 2-64): "))
        except ValueError:
            print("Error: Ingrese valores numéricos enteros. Inténtelo de nuevo.")
            continue

        if not (2 <= N <= 64) or not (2 <= B <= 64):
            print("Error: Las bases deben estar entre 2 y 64. Inténtelo de nuevo.")
            continue

        # Control de overflow
        capacidad_actual = N ** R
        if C >= capacidad_actual:
            print(f"\n[ALERTA] OVERFLOW DETECTADO: R={R} en Base {N} soporta hasta {capacidad_actual - 1}.")
            R = calcular_r_minimo(C, N)
            print(f"[OK] El sistema se expandió a R={R} dígitos para la carga.\n")
        else:
            print(f"\n[OK] Capacidad suficiente con R={R}.\n")

        digitos = [0] * R

        encabezado = " | ".join([f"D{i}" for i in range(R - 1, -1, -1)])
        print(encabezado)
        print("-" * len(encabezado))

        delay = 0.005 if C <= 200 else 0.0001

        # Conteo progresivo
        for paso in range(1, C + 1):
            digitos[0] += 1

            indice = 0
            while digitos[indice] == N:
                digitos[indice] = 0
                indice += 1

                if indice == len(digitos):
                    digitos.append(0)
                    R += 1

                digitos[indice] += 1

            estado_visual = " | ".join([ALFABETO[d] for d in reversed(digitos)])
            print(f"\r{estado_visual}", end="", flush=True)

            if delay > 0:
                time.sleep(delay)

        print("\n")

        # Conversión directa del valor acumulado a Base B
        valor_base_10 = C
        print(f"=== PROCESO DE CONVERSIÓN A BASE {B} ===")
        temp_b = valor_base_10
        resultado_base_b = ""

        if temp_b == 0:
            resultado_base_b = ALFABETO[0]
        else:
            paso_b = 1
            while temp_b > 0:
                residuo_b = temp_b % B
                cociente_b = temp_b // B
                caracter_b = ALFABETO[residuo_b]
                resultado_base_b = caracter_b + resultado_base_b

                print(f"  Paso {paso_b} -> {temp_b} / {B}:")
                print(f"    Cociente: {cociente_b} | Residuo: {residuo_b} (Símbolo: '{caracter_b}') | Acumulado: {resultado_base_b}")

                temp_b = cociente_b
                paso_b += 1

        # Verificación del estado final
        verificacion_base_10 = sum(d * (N ** i) for i, d in enumerate(digitos))
        resultado_base_n = "".join([ALFABETO[d] for d in reversed(digitos)])

        print("\n=== RESULTADO ===")
        print(f"-> Resultado final en Base del contador (Base {N}): {resultado_base_n}")
        print(f"-> Resultado en Base destino (Base {B}): {resultado_base_b}")
        print(f"-> Verificación en Base 10: {verificacion_base_10} (Esperado: {valor_base_10})")

        print("\n" + "=" * 40)
        repetir = input("¿Deseas realizar otro conteo? (s/n): ").strip().lower()
        if repetir != 's':
            print("Finalizando sistema.")
            break


if __name__ == "__main__":
    contar_y_convertir()
