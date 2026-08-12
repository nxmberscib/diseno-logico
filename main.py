import math
import time

# Generación del alfabeto Base 64 con la Ñ y ñ en su posición correcta
digitos_ascii = "".join(chr(i) for i in range(48, 58))  # 0-9 (10)

# Mayúsculas: A-N (65-78), Ñ (209), O-Z (79-90) -> 27 caracteres
mayus_antes = "".join(chr(i) for i in range(65, 79))
mayus_despues = "".join(chr(i) for i in range(79, 91))
mayusculas = mayus_antes + chr(209) + mayus_despues

# Minúsculas: a-n (97-110), ñ (241), o-z (111-122) -> 27 caracteres
minus_antes = "".join(chr(i) for i in range(97, 111))
minus_despues = "".join(chr(i) for i in range(111, 123))
minusculas = minus_antes + chr(241) + minus_despues

ALFABETO = digitos_ascii + mayusculas + minusculas


def contar_y_convertir():
    while True:
        print("\n=== SISTEMA DE CONTEO UNIVERSAL ===")

        # Entrada de datos
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

        # Detección de overflow y adaptación de R
        capacidad_actual = N ** R
        if C >= capacidad_actual:
            print(f"\n[ALERTA] OVERFLOW DETECTADO: El sistema con R={R} soporta hasta {capacidad_actual - 1} conteos.")
            print("Adaptando el sistema automáticamente...")

            R_necesario = math.ceil(math.log(C + 1, N))
            R = R_necesario
            print(f"[OK] El sistema se ha expandido a R={R} dígitos para soportar la carga.\n")
        else:
            print(f"\n[OK] Capacidad suficiente. El sistema soporta los conteos con R={R}.\n")

        # Inicialización del sistema
        digitos = [0] * R

        encabezado = " | ".join([f"D{i}" for i in range(R - 1, -1, -1)])
        print(encabezado)
        print("-" * len(encabezado))

        # Bucle de conteo (Odómetro)
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
            time.sleep(0.005)

        print()

        # 1. GUÍA VISUAL DEL ALFABETO BASE 64 COMPLETO
        print("\n" + "=" * 15 + " GUÍA VISUAL DEL ALFABETO BASE 64 " + "=" * 15)
        print(" Digitos (0-9):    " + " ".join([f"{i}:{ALFABETO[i]}" for i in range(10)]))
        print(" Mayús   (10-36):  " + " ".join([f"{i}:{ALFABETO[i]}" for i in range(10, 37)]))
        print(" Minús   (37-63):  " + " ".join([f"{i}:{ALFABETO[i]}" for i in range(37, 64)]))
        print("=" * 60 + "\n")

        valor_base_10 = C

        # 2. GUÍA VISUAL DEL ALFABETO DELIMITADO A LA BASE B
        print(f"=== GUÍA VISUAL DEL ALFABETO DELIMITADO A LA BASE DESTINO (Base {B}) ===")
        print(f"Mostrando los {B} símbolos válidos extraídos de la Base 64 (del valor 0 al {B - 1}):")

        alfabeto_base_b = ALFABETO[:B]
        for i in range(0, B, 10):
            fin = min(i + 10, B)
            bloque = " ".join([f"[{j}:{alfabeto_base_b[j]}]" for j in range(i, fin)])
            print(f" Rango {i:2d}-{fin - 1:2d}: {bloque}")
        print("-" * 65 + "\n")

        # 3. Proceso detallado de conversión a Base B
        print(f"=== PROCESO DE CONVERSIÓN A BASE {B} ===")
        temp_b = valor_base_10
        resultado_base_b = ""

        if temp_b == 0:
            resultado_base_b = ALFABETO[0]
            print(f"El valor es 0, resultado directo: {resultado_base_b}")
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

        # 4. Proceso de Verificación detallado en Base 10
        print("\n=== PROCESO DE VERIFICACIÓN EN BASE 10 ===")
        print(f"Expandiendo el número en Base {N} a Base 10 (Suma de dígitos por potencias de la base):")

        verificacion_base_10 = 0
        for i, d in enumerate(digitos):
            peso = N ** i
            parcial = d * peso
            verificacion_base_10 += parcial
            simbolo = ALFABETO[d]
            print(f"  D{i} ('{simbolo}' = {d}) * ({N}^{i} = {peso}) = {parcial}")

        resultado_base_n = "".join([ALFABETO[d] for d in reversed(digitos)])

        # Resumen final
        print("\n=== RESUMEN FINAL ===")
        print(f"-> Resultado final en la Base del contador (Base {N}): {resultado_base_n}")
        print(f"-> Resultado convertido a la Base destino (Base {B}): {resultado_base_b}")
        print(f"-> Verificación calculada en Base 10: {verificacion_base_10} (Valor real esperado: {valor_base_10})")

        # Preguntar si se desea realizar un nuevo conteo
        print("\n" + "=" * 40)
        repetir = input("¿Deseas realizar otro conteo? (s/n): ").strip().lower()
        if repetir != 's':
            print("¡Nos vemos! Finalizando sistema.")
            break


if __name__ == "__main__":
    contar_y_convertir()