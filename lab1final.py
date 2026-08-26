import os
import sys
import time

if os.name == "nt":
    os.system("")

ALFABETO = "0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZabcdefghijklmnñopqrstuvwxyz"


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def calcular_r_minimo(C, N):
    if C == 0:
        return 1
    r, capacidad = 0, 1
    while capacidad <= C:
        capacidad *= N
        r += 1
    return r


def obtener_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  Error: Ingrese un entero válido.")


def contar_y_convertir():
    while True:
        limpiar_pantalla()
        print("===========================================")
        print("       SISTEMA DE CONTEO UNIVERSAL        ")
        print("===========================================\n")

        R = obtener_entero("Ingrese R (Dígitos iniciales): ")
        C = obtener_entero("Ingrese C (Total de conteos): ")
        N = obtener_entero("Ingrese N (Base de conteo [2-64]): ")
        B = obtener_entero("Ingrese B (Base de conversión [2-64]): ")

        if not (2 <= N <= 64 and 2 <= B <= 64):
            print("\nError: Las bases deben estar en el rango [2, 64].")
            input("\nPresione ENTER para reintentar...")
            continue

        capacidad_actual = N**R
        if C >= capacidad_actual:
            R = calcular_r_minimo(C, N)
            print(f"\n[OVERFLOW] Para contar hasta {C} en Base {N}, R se expandió a {R} dígitos.")
        else:
            print(f"\nCapacidad suficiente para el conteo con R={R}.")

        input("\nPresione ENTER para iniciar el proceso...")
        limpiar_pantalla()

        # Bloque de visualización del alfabeto
        print("===========================================")
        print(f"   TABLA DE SÍMBOLOS - BASE {N} (0 al {N-1})")
        print("===========================================")
        chunk = 16
        for i in range(0, N, chunk):
            limite = min(i + chunk, N)
            valores = range(i, limite)
            fila_val = " | ".join(f"{v:2}" for v in valores)
            fila_sim = " | ".join(f"{ALFABETO[v]:>2}" for v in valores)
            print(f"Valor:   {fila_val}")
            print(f"Símbolo: {fila_sim}")
            if limite < N:
                print("-" * len(f"Valor:   {fila_val}"))
        print("===========================================\n")

        # Bloque de conteo en vivo
        print("===========================================")
        print("                  CONTEO                   ")
        print("===========================================\n")

        digitos = [0] * R
        intervalo_refresco = 1.0 / 30.0
        ultimo_refresco = time.perf_counter()
        primer_frame = True

        for paso in range(1, C + 1):
            digitos[0] += 1
            idx = 0
            while digitos[idx] == N:
                digitos[idx] = 0
                idx += 1
                if idx == len(digitos):
                    digitos.append(0)
                    R += 1
                digitos[idx] += 1

            tiempo_actual = time.perf_counter()
            if tiempo_actual - ultimo_refresco >= intervalo_refresco or paso == C:

                max_idx = R - 1
                while max_idx > 0 and digitos[max_idx] == 0:
                    max_idx -= 1

                ceros_ocultos = R - 1 - max_idx
                info_ocultos = f"[Ceros omitidos: {ceros_ocultos}]" if ceros_ocultos > 0 else "[Todos en uso]"

                encabezados = []
                valores = []
                for i in range(max_idx, -1, -1):
                    header = f"D{i}"
                    val = ALFABETO[digitos[i]]
                    ancho = max(len(header), len(val))
                    encabezados.append(f"{header:>{ancho}}")
                    valores.append(f"{val:>{ancho}}")

                str_encabezado = " | ".join(encabezados)
                str_valores = " | ".join(valores)
                separador = "-" * len(str_encabezado)

                if not primer_frame:
                    sys.stdout.write("\033[4A")
                else:
                    primer_frame = False

                sys.stdout.write(f"Progreso: {paso}/{C} | {info_ocultos}".ljust(100) + "\n")
                sys.stdout.write((" " + str_encabezado).ljust(100) + "\n")
                sys.stdout.write((" " + separador).ljust(100) + "\n")
                sys.stdout.write((" " + str_valores).ljust(100) + "\n")
                sys.stdout.flush()

                ultimo_refresco = tiempo_actual

            time.sleep(1 / 900)

        print("\n")
        input("Conteo completado. Presione ENTER para ver la conversión...")

        # Bloque de conversión a Base B
        limpiar_pantalla()
        print("=========================================================================")
        print(f"                     CONVERSIÓN (BASE 10 A BASE {B})")
        print("=========================================================================\n")

        temp_b = C
        resultado_base_b = ""

        if temp_b == 0:
            resultado_base_b = ALFABETO[0]
            print(f"  Paso 1: Valor 0 -> Símbolo: '{ALFABETO[0]}'")
        else:
            paso_b = 1
            print(f"{'Paso':<6} | {'Ecuación (Dividendo = Cociente * Base + Residuo)':<50} | {'Símbolo':<9} | {'Acumulado'}")
            print("-" * 92)

            while temp_b > 0:
                residuo = temp_b % B
                cociente = temp_b // B
                caracter = ALFABETO[residuo]
                resultado_base_b = caracter + resultado_base_b

                ecuacion = f"{temp_b} = {cociente} * {B} + {residuo}"
                info_simbolo = f"{residuo} -> '{caracter}'"

                print(f"{paso_b:<6} | {ecuacion:<50} | {info_simbolo:<9} | {resultado_base_b}")

                temp_b = cociente
                paso_b += 1

        print("\n")
        input("Conversión completada. Presione ENTER para ver la verificación...")

        # Bloque de verificación paso a paso (Base N a Base 10)
        limpiar_pantalla()
        print("=========================================================================")
        print(f"                   VERIFICACIÓN (BASE {N} A BASE 10)")
        print("=========================================================================\n")

        max_idx_ver = len(digitos) - 1
        while max_idx_ver > 0 and digitos[max_idx_ver] == 0:
            max_idx_ver -= 1

        suma_verificacion = 0
        resultado_base_n = "".join([ALFABETO[d] for d in reversed(digitos)])

        print(f"{'Posición':<10} | {'Símbolo':<9} | {'Valor':<7} | {'Potencia (Base^Pos)':<20} | {'Subtotal'}")
        print("-" * 75)

        for i in range(max_idx_ver, -1, -1):
            valor_pos = digitos[i]
            peso = N**i
            subtotal = valor_pos * peso
            suma_verificacion += subtotal

            info_potencia = f"{N}^{i} = {peso}"
            info_simbolo = f"'{ALFABETO[valor_pos]}'"

            print(f"D{i:<9} | {info_simbolo:<9} | {valor_pos:<7} | {info_potencia:<20} | {subtotal}")

        print("-" * 75)
        print(f"{'SUMA TOTAL EN BASE 10:':<53} {suma_verificacion}")

        # Resumen Final
        print("\n=========================================================================")
        print("                               RESULTADOS                                ")
        print("=========================================================================")
        print(f"  • Valor contado (Base 10) : {C}")
        print(f"  • Base Origen (Base {N})   : {resultado_base_n.lstrip(ALFABETO[0]) or ALFABETO[0]}")
        print(f"  • Base Destino (Base {B})  : {resultado_base_b}")
        print(f"  • Verificación exitosa    : {'SÍ' if suma_verificacion == C else 'NO'}")
        print("=========================================================================")

        repetir = input("\n¿Desea realizar otro cálculo? (s/n): ").strip().lower()
        if repetir != "s":
            limpiar_pantalla()
            break


if __name__ == "__main__":
    contar_y_convertir()
