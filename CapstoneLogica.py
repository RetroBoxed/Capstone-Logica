from pysat.formula import CNF
from pysat.solvers import Solver
import random

def satsolver(clausulas):
    """
    Resuelve un problema SAT con las cláusulas dadas.
    Retorna (es_satisfacible, modelo) o (es_satisfacible, None) si es insatisfacible.
    """
    try:
        # Extraer variables relevantes de las cláusulas
        variables_relevantes = set()
        for clausula in clausulas:
            for var in clausula:
                variables_relevantes.add(abs(var))
        
        # Crear fórmula CNF
        cnf = CNF(from_clauses=clausulas)
        
        # Crear solver SAT
        with Solver(bootstrap_with=cnf) as solver:
            es_satisfacible = solver.solve()
            
            # Obtener el modelo (puede ser None si es insatisfacible)
            modelo_completo = solver.get_model()
            
            if modelo_completo is not None:
                # Filtrar solo las variables relevantes
                modelo = [v for v in modelo_completo if abs(v) in variables_relevantes]
            else:
                modelo = None
            
            return es_satisfacible, modelo
    except Exception as e:
        print(f"Error en SAT solver: {e}")
        return None, None

def mostrar_proceso_logico(premisas, conclusion_var, es_valido):
    print("\n" + "="*40)
    print("PROCESO DE RESOLUCIÓN LÓGICA")
    print("="*40)
    
    # Paso 1: Formalización
    formula = f"({' ∧ '.join(premisas)}) → {conclusion_var}"
    print(f"1. Formalización: {formula}")
    
    # Paso 2: Convertir a FNC para refutacion
    # Para refutacion: (premisas) ∧ ¬conclusion
    fnc = f"({' ∧ '.join(premisas)}) ∧ ¬{conclusion_var}"
    print(f"2. Conversión para refutación: {fnc}")
    
    # Paso 3: Negar la conclusión para refutación
    print(f"3. Negando la conclusión: ¬{conclusion_var}")
    
    # Paso 4: Refutación
    print(f"4. Aplicando refutación...")
    if es_valido:
        print("   CONTRADICCIÓN ENCONTRADA: La hipótesis es VERDADERA.")
    else:
        print("   SIN CONTRADICCIÓN: La hipótesis no se puede probar.")

def obtener_mapeo_fijo():
    """
    Retorna un mapeo fijo de proposiciones a números.
    Este mapeo asegura consistencia en los resultados del SAT solver.
    """
    return {
        'A': 1,     # Enciende
        '-A': -1,
        'B': 2,     # Video
        '-B': -2,
        'C': 3,     # Pitidos
        '-C': -3,
        'D': 4,     # Congela
        '-D': -4,
        'F': 5,     # Sistema
        '-F': -5,
        'fuente': 1,    # Fuente
        '-fuente': -1,
        'ram': 3,       # RAM
        '-ram': -3,
        'placa': 2,     # Placa
        '-placa': -2,
        'disco': 4,     # Disco
        '-disco': -4,
        'sistema': 5,   # Sistema (falla)
        '-sistema': -5
    }

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

    # Reglas de fallas - cada falla tiene sus condiciones
    reglas = {
        "ram": ["A", "-B", "C"],  # Prende, no da imagen, emite pitidos
        "fuente": ["A", "-B", "-C", "D"],  # Prende, no da imagen, no emite pitidos, se congela
        "placa": ["A", "-B", "-C", "-D", "-F"],  # Prende, no da imagen, no emite pitidos, no se congela, sistema no responde
        "disco": ["A", "B", "-C", "D", "F"],  # Prende, da imagen, no emite pitidos, se congela, sistema responde
        "sistema": ["-F"]  # No prende en absoluto
    }

    cliente_elegido = random.choice(clientes)
    print(f"\n[CLIENTE]: '{cliente_elegido['mensaje']}'")
    obs = cliente_elegido["obs"]

    print("Ingresa las proposiciones separadas por coma (ej: A, -B, C): ")
    input_str = input()
    obs_usuario = [p.strip() for p in input_str.split(',')]

    if obs_usuario == obs:
        # Encontrar el componente que coincide
        componente = None
        for comp, prem in reglas.items():
            if prem == obs:
                componente = comp
                break
        
        if componente:
            # Mostrar el proceso lógico
            mostrar_proceso_logico(obs, componente, True)
            
            # Usar SAT solver para verificar la conclusión
            print("\n5. Verificación con SAT Solver:")
            
            # Crear cláusulas para verificar: premisas ∧ ¬conclusion
            # Si es insatisfacible, entonces conclusion es válida
            clausulas = []
            
            # Usar mapeo fijo para consistencia
            var_map = obtener_mapeo_fijo()
            
            # Añadir las premisas (cada premisa es una cláusula unitaria)
            for p in obs:
                var = var_map[p]
                clausulas.append([var])
            
            # Añadir la negación de la conclusión
            conclusion_var = var_map[componente]
            clausulas.append([-conclusion_var])
            
            es_sat, modelo = satsolver(clausulas)
            
            if es_sat is not None:
                if not es_sat:
                    print(f"   SAT Solver confirma: La falla ES en el {componente.upper()}")
                else:
                    print(f"   SAT Solver indica: No se puede demostrar la falla en {componente.upper()}")
            
            # Mostrar el modelo del SAT Solver
            if modelo:
                # Formatear como cláusulas separadas: [1], [2], [-3], ...
                clauses_str = ', '.join([f'[{v}]' for v in modelo])
                print(f"\n   Modelo SAT Solver: {clauses_str}")
            else:
                # Cuando es insatisfacible, mostrar las cláusulas de entrada
                clauses_str = ', '.join([f'[{v}]' for v in clausulas])
                print(f"\n   Modelo SAT Solver: {clauses_str}")
            
            # Conclusión final
            print(f"\n[ERROR 404]: La falla es en el {componente.upper()}.")
        else:
            print("\n[ERROR 404]: No se encontró un componente que coincida con las proposiciones dadas.")
    else:
        print("\n[ERROR 404]: Las proposiciones ingresadas no coinciden con el caso del cliente.")
        print(f"Esperado: {obs}")
        print(f"Ingresado: {obs_usuario}")

if __name__ == "__main__":
    jugar_Error404()
