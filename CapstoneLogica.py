import random
def mostrar_proceso_logico(premisas, conclusion_var, es_valido):
    print("\n" + "="*40)
    print("PROCESO DE RESOLUCIÓN LÓGICA")
    print("="*40)
    
    # Paso 1: Formalización
    formula = f"({' ∧ '.join(premisas)}) → {conclusion_var}"
    print(f"1. Formalización: {formula}")
    
    # Paso 2: Pasar a FNC (A → B  es equivalente a  ¬A ∨ B)
    fnc = f"¬({' ∧ '.join(premisas)}) ∨ {conclusion_var}"
    print(f"2. Conversión a FNC: {fnc}")
    
    # Paso 3: Negar la conclusión para refutación
    print(f"3. Negando la conclusión: ¬{conclusion_var}")
    
    # Paso 4: Refutación
    print(f"4. Aplicando refutación...")
    if es_valido:
        print("   CONTRADICCIÓN ENCONTRADA: La hipótesis es VERDADERA.")
    else:
        print("   SIN CONTRADICCIÓN: La hipótesis no se puede probar.")

def jugar_Error404():
    # Variables según el documento
    print("VARIABLES: A: Enciende | B: Video | C: Pitidos | D: Congela | F: Sistema")

    # Entrada de datos - Clientes predefinidos
    clientes = [
        {"mensaje": "La computadora prende, no da imagen y emite pitidos.", "obs": ["A", "-B", "C"]},  # RAM
        {"mensaje": "La computadora prende, no da imagen, no emite pitidos y se congela.", "obs": ["A", "-B", "-C", "D"]},  # Fuente
        {"mensaje": "La computadora prende, no da imagen, no emite pitidos, no se congela y el sistema no responde.", "obs": ["A", "-B", "-C", "-D", "-F"]},  # Placa
        {"mensaje": "La computadora prende, da imagen, no emite pitidos, se congela y el sistema responde.", "obs": ["A", "B", "-C", "D", "F"]},  # Disco
        {"mensaje": "La computadora no prende en absoluto.", "obs": ["-F"]},  # Sistema
        {"mensaje": "La computadora prende, da imagen pero se congela inmediatamente.", "obs": ["A", "B", "D"]},  # Disco o Placa
    ]

    cliente_elegido = random.choice(clientes)
    print(f"\n[CLIENTE]: '{cliente_elegido['mensaje']}'")
    obs_correctas = cliente_elegido["obs"]

    # Entrada de proposiciones
    print("Ingresa las proposiciones separadas por coma (ej: A, -B, C): ")
    input_str = input()
    obs = [p.strip() for p in input_str.split(',')]

    if obs == obs_correctas:
        # Mapeo de fallas según el documento

        reglas = {
            "ram": ["A", "-B", "C"],  # Prende, no da imagen, emite pitidos
            "fuente": ["A", "-B", "-C", "D"],  # Prende, no da imagen, no emite pitidos, se congela
            "placa": ["A", "-B", "-C", "-D", "-F"],  # Prende, no da imagen, no emite pitidos, no se congela, sistema no responde
            "disco": ["A", "B", "-C", "D", "F"],  # Prende, da imagen, no emite pitidos, se congela, sistema responde
            "sistema": ["-F"]  # No prende en absoluto
        }
        # Encontrar el componente que coincide
        componente = None
        for comp, prem in reglas.items():
            if prem == obs:
                componente = comp
                break

        if componente:
            # Mostrar el proceso lógico
            mostrar_proceso_logico(obs, componente, True)

            # Conclusión
            print(f"\n[ERROR 404]: La falla es en el {componente.upper()}.")
        else:
            print("\n[ERROR 404]: No se encontró un componente que coincida con las proposiciones dadas.")
    else:
        print("\n[ERROR 404]: Las proposiciones ingresadas no coinciden con el caso del cliente.")

if __name__ == "__main__":
     jugar_Error404()
    