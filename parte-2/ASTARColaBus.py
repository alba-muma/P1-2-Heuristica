import ast
import sys
import time


def a_estrella(nodo_inicial, heuristica_elegida):
    #Comenzamos el contador para ver el tiempo total
    t1 = time.time()

    # Iniciamos la lista abierta donde estaran los nodos sucesores
    #cerrada = []
    abierta = []
    abierta.append(nodo_inicial)
    # Variable que indica si se ha encontrado solucion o no
    exito = False
    # Variable que cuenta los nodos expandidos
    nodos_expandidos = 1

    # Mientras haya nodos en abierta o no se encuentre solucion
    while len(abierta) > 0 and not exito:
        # Se coge el primer elemento de abierta
        n = abierta.pop(0)
        #cerrada.append(n)
        # Se obtienen los costes del nodo y del padre
        coste_nodo = n.coste_nodo
        coste_padre = n.coste

        # Si no hay alumnos en la cola, se habra obtenido una solcion
        if len(n.no_cola) == 0:
            exito = True
        else:
            for alumno , asiento in n.no_cola.items():
                coste = coste_padre
                # Actualizamos la cola para el sucesor añadiendo al alumno
                cola_sucesor = n.cola.copy()
                cola_sucesor[alumno] = asiento
                # Actualizamos la no cola para el sucesor eliminando al alumno
                no_cola_sucesor = n.no_cola.copy()
                del no_cola_sucesor[alumno] 
                # Actualizamos su coste
                coste_alumno_actual = coste_alumno(alumno, asiento, n.cola , n.no_cola , coste_nodo)
                # Se actualiza el coste total
                coste += coste_alumno_actual
                # Actualizamos su heuristica , cogemos la heuristica que nos hayan indicado por parametro
                if heuristica_elegida == "1":
                    heuristica = heuristica1(no_cola_sucesor)
                elif heuristica_elegida == "2":
                    heuristica = heuristica2(no_cola_sucesor)
                else:
                    # Solo tenemos dos heuristicas, todo lo demas dara error
                    print("Error")
                    return -1
                # Creamos el nodo con sus respectivas colas
                # Si el coste y la heuristica es muy alto no se añadira el nodo porque esta haciendo un movimiento invalido
                if coste + heuristica < 1000000000:
                    nodo_sucesor = nodo(cola_sucesor , no_cola_sucesor , coste , heuristica , coste_nodo, coste_padre) 
                    # Añadimos a el sucesor a abierta
                    abierta.append(nodo_sucesor)
                    # Actualizamos el contador de nodos_expandidos
                    nodos_expandidos += 1
            # Ordenamos la lista
            abierta = quick_sort(abierta)
    
    if exito == True: 
        # Tiempo cuando termina 
        t2 = time.time()
        # Devolvemos el nodo_meta , el tiempo de ejecución y el numero de nodos expandidos
        return [ n , (t2 - t1) , nodos_expandidos ]
    else:
        t2 = time.time()
        return [ False , (t2 - t1) , nodos_expandidos ]

def coste_alumno (alumno, asiento, cola, no_cola, alum_anterior):
    coste = 1
    if alumno[-1] == "R":
        if len(no_cola) == 1:
            # Si ya no hay alumnos que puedan ayudar al alumno con movilidad reducida
            coste = 1000000000
        else:
            # Si el alumno con movilidad reducida puede ser ayudado por un alumno sin movilidad reducida el coste es 3
            coste = 3

    if len(cola) != 0: # Si no hay alumnos en la cola no se podrá ayudar a un alumno con movilidad reducida
        claves = list(cola.keys())
        ultimo_elem = claves[-1]
        if ultimo_elem[-1] == "R" and alumno[-1] != "R": #Si el anterior es un alumno con movilidad reducida
            coste = 0
        if alumno[-1] == "R" and ultimo_elem[-1] == "R": # Si hay dos alumnos de movlidad reducida seguidas no se podrán ayudar
            coste = 1000000000
        if ultimo_elem[-2] == "C": # Si el alumno anterior es conflictivo se multiplica x2 tu coste
            coste = coste *2 

    for conflictivo , asiento_conflic in cola.items(): 
        if conflictivo[-2] == "C":
            if asiento_conflic < asiento: # Si hay un conflictivo delante sentado el coste se multiplicará por dos
                coste = coste * 2

    if alumno[-2] == "C": # Si el alumno es conflictivo se duplica el coste el alumno anterior
        coste = coste + alum_anterior
   
    return coste

def quick_sort(arr):
  if len(arr) <= 1:
    return arr

  pivot = arr[len(arr) // 2]  # elegimos el elemento del medio como pivote
  left = []  # lista para los elementos menores que el pivote
  right = []  # lista para los elementos mayores que el pivote
  middle = []

  # recorremos la lista original y agregamos los elementos a la izquierda o derecha según corresponda
  for x in arr:
    if x.funcion_orden < pivot.funcion_orden:
      left.append(x)
    elif x.funcion_orden > pivot.funcion_orden:
      right.append(x)
    else:
        middle.append(x)

  # aplicamos recursivamente el algoritmo de ordenamiento rápido a las sublistas
  left = quick_sort(left)
  right = quick_sort(right)

  # combinamos las sublistas ordenadas y agregamos el pivote en medio
  return left + middle + right

def heuristica1 (no_cola):
    h = 0
    # Variables que contabilizan el numero de alumnos con movilidad reducidad y sin 
    movilidad = 0
    alumno = 0
    for alum in no_cola.keys():
        h += 1
        if alum[-1] == "R":
            movilidad += 1
            # Si el alumno es de movilidad reducida se añade uno mas 
            # (acaban siendo 3 coste: 2 coste del alumno de movilidad + 1 alumno que ayuda)
            h += 1
        else:
            alumno += 1
    # Si hay mas alumnos con movilidad reducida que sin no podrán ser ayudados
    if movilidad > alumno:
        h = 1000000000
    return h

def heuristica2 (no_cola):
    h = 0
    for _ in no_cola.keys():
        # se suma uno a la heuristica por cada alumno que queda por asignar a la cola
        h += 1
    return h


class nodo ():
    def __init__ (self, cola , no_cola , coste , heuristica, coste_alum, coste_padre):
    # Constructor del nodo
        # Dicc de alumnos que están en la cola
        self.cola = cola
        # Dicc de alumonos que no estan en la cola
        self.no_cola = no_cola
        # Heuristica del nodo
        self.heuristica = heuristica
        # Coste del nodo
        self.coste = coste
        # Fucion de ordenacion
        self.funcion_orden = self.heuristica + self.coste
        # Coste del alumno anterior
        self.coste_alum_anterior = coste_alum
        # Coste del nodo sin acumular
        self.coste_nodo = self.coste - coste_padre

# Variable con la direccion del fichero donde están los parametors
path = sys.argv[1]
# Abrimos el fichero
fichero = open(path)
# La heuristica que tenemos que aplicar está en el segundo parametro
heuristica = sys.argv[2]
# Leemos el archivo de entrada
alumnos_str = fichero.read()
# Convertimos lo que hay en el archivo en un dicc
alumnos = ast.literal_eval(alumnos_str)

# Creamos el nodo inicial
nodo_inicial = nodo( {} , alumnos , 0 , 0 , 0 , 0)

# Ejecutamos la funcion astar
datos = a_estrella(nodo_inicial, heuristica)

# Obtenemos todos los valores del resultado
nodo_meta = datos[0]
tiempo = datos[1]
nodos_expandidos_totales = datos[2]

if nodo_meta != False:  
    coste_total = nodo_meta.coste
    cola_obtenida = nodo_meta.cola
else: 
    # Si no hay solucion
    coste_total = "No hay solucion"
    cola_obtenida = "No hay solucion"

# Escribimos en el fichero de la solucion
fichero_solucion = open(path + str(heuristica) + ".output" , "w")
fichero_solucion.write ("INICIAL: " + str(alumnos) + "\n")
fichero_solucion.write ("FINAL: " + str(cola_obtenida))

# Escribimos en el fichero de estadisticas el tiempo, los nodos de ejecucion, coste y longitud
fichero_stat = open(path + str(heuristica) + ".stat" , "w")
fichero_stat.write ("Tiempo total: " + str(int(tiempo)) + "\n")
fichero_stat.write ("Coste total: " + str(coste_total) + "\n")

if nodo_meta == False:
    fichero_stat.write ("Longitud del plan: " + str(cola_obtenida) + "\n")
else:
        fichero_stat.write ("Longitud del plan: " + str(len(cola_obtenida)) + "\n")
fichero_stat.write ("Nodos expandidos: " + str(nodos_expandidos_totales))