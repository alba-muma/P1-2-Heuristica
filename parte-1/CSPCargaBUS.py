"""
Codigo realizado por: 
    Juan Miguel Pulgar Esquivel 100451036
    Alba Marco Ugarte 100451139

"""
from constraint import *
import sys
import random
# Declaracion del problema
problem = Problem()

alumnos = []
# Subconjuntos de los asientos de arriba, abajo, izquierda y derecha, sin contar las esquinas
l_arriba = [25, 21, 17, 13, 9, 5]
l_abajo = [28, 24, 20, 16, 12,8]
l_izq = [30, 31]
l_der = [2, 3]
# Subconjunto de los asientos del pasillo
pasillo = [2, 6, 10, 14, 18, 22, 26, 30, 3, 7, 11, 15, 19, 23, 27, 31]

# Recoge el path del fichero de entrada según lo que se ponga en la terminal
path = sys.argv[1]
# Abre el fichero de entrada
fichero = open(path)
# Lee las lineas del fichero de entrada
lineas = fichero.readlines()
# Añade los elementos necesarios del problema a una lista, ya que nuestras variables deben ser como se han descrito en el modelo
for linea in lineas:
    alumnos.append ([linea[0], linea[2], linea[4], linea[6], linea[8]])

def tiene_hermano_pequeño(alumno):
    for n in alumnos:
        # Si el elemento 4 del alumno (que indica si tiene un hermano) es igual a la id de su hermano y el hermano es del ciclo 1 -
        # significa que tiene hermano pequeño (esta función solo se ejecuta cuando alumno es del curso 2.
        if alumno[4] == n[0] and n[1] == "1":
            return True
    else:
        return False
# Añadimos las variables del problema
for alumno in alumnos:
    # Si es un alumno con movilidad reducida se le asignara un asiento especial.
    if alumno[3] == "R":

        # Si es del ciclo 2 y no tiene un hermano pequeño se le asignará un asiento de la parte trasera.
        if alumno[1] == "2" and tiene_hermano_pequeño(alumno) == False:
            problem.addVariable(alumno[0], [17, 18, 19, 20])
        # Si es del ciclo 1 solo se le asignarán los de la parte delantera.
        else:
            problem.addVariable(alumno[0], [1, 2, 3, 4, 13, 14, 15, 16])
    else:
        # Si no es de movilidad reducida y es del ciclo 1 irá en la parte delantera.
        if alumno[1] == "1":
            problem.addVariable(alumno[0], range(1,  17))
        # Si es del ciclo 2 irá en la parte delantera si tiene un hermano pequeño, y en la trasera en cualquier otro caso.
        else:
            if tiene_hermano_pequeño(alumno):
                problem.addVariable(alumno[0], range(1, 17))
            else:
                problem.addVariable(alumno[0], range(17, 33))

# Función que comprueba que no haya dos alumnos asignados al mismo asiento
def no_iguales(a, b):
    if a != b:
        return True
    return False

# Funcion que comprueba que nadie se siente al lado de alguien con movilidad reducida
def movilidad_solo (a, b):
    # Si el sitio es par el asiento con un valor de uno por debajo deberá estar vacío
    if a % 2 == 0 and b+1 != a:
        return True
    # Si el sitio es impar el asiento con un valor de uno por encima deberá estar vacío
    elif a % 2 != 0 and b-1 != a:
        return True

# Funcion que comprueba que ningun alumno conflictivo se sienta cerca de otro alumno conflictivo o de un alumno con movilidad reducida
def conflictivo_solo (a , b):
    # Como pone en las restricciones, si está en la parte de arriba, el otro alumno no podrá sentarse en esos 5 sitios de alrededor
    if a in l_arriba:
        if b != a+1 and b != a-4 and b != a-3 and b != a+4 and b != a+5:
            return True
    # Si está abajo, el otro alumno no podrá sentarse en esos 5 sitios de alrededor
    elif a in l_abajo:
        if b != a-1 and b != a-4 and b != a-5 and b != a+4 and b != a+3:
            return True
    # Si está en la izquierda, el otro alumno no podrá sentarse en esos 5 sitios de alrededor
    elif a in l_izq:
        if b != a+1 and b != a-1 and b != a-4 and b != a-5 and b != a-3:
            return True
    # Si está en la derecha, el otro alumno no podrá sentarse en esos 5 sitios de alrededor
    elif a in l_der:
        if b != a+1 and b != a-1 and b != a+4 and b != a+5 and b != a+3:
            return True
    # Si está en la esquina con valor 1, no podrá sentarse en los asientos 2, 5 y 6
    elif a == 1:
        if b not in [5, 2, 6]:
            return True
    # Si está en la esquina con valor 4, no podrá sentarse en los asientos 3, 7 y 8
    elif a == 4:
        if b not in [8, 3, 7]:
            return True
    # Si está en la esquina con valor 32, no podrá sentarse en los asientos 27, 28 y 31
    elif a == 32:
        if b not in [31, 28, 27]:
            return True
    # Si está en la esquina con valor 4, no podrá sentarse en los asientos 25, 26 y 30
    elif a == 29:
        if b not in [30, 25, 26]:
            return True
    # Si está en un asiento central, el otro alumno no podrá sentarse en los 8 sitios que tiene alrededor.
    else:
        if b not in [a+1 , a-1 , a+4 , a-4 , a+5 , a-5 , a+3 , a-3]:
            return True
# Función que hace que los hermanos tengan que sentarse juntos
def hermanos_juntos(a , b):
    # Si un hermano está en un sitio par, el otro se sentará en el sitio con un valor de 1 por debajo
    if a % 2 == 0 and b == a-1:
        return True
    # Si un hermano está en un sitio impar, el otro se sentará en el sitio con un valor de 1 por encima
    elif a % 2 != 0 and b == a+1:
        return True
    return False
# Función que hace que el hermano mayor tenga que sentarse en el pasillo
def mayor_pasillo(a, b):
    # El hermano mayor debe estar en el pasillo y el menor en la ventana
    if a in pasillo and b not in pasillo:
        return True

#Bucle que añade las restricciones
for alumno in alumnos:

    for alumno2 in alumnos:
        # Solo se ejecuta si a y b son distintos alumnos, como se indica en el modelo
        if alumno != alumno2:
            # Se añade una restricción para que 2 alumnos no puedan sentarse en el mismo lugar
            problem.addConstraint(no_iguales, (alumno[0] , alumno2[0]))
            # Si un alumno es de movilidad reducida, se ejecuta la función que hace que no se pueda sentar nadie a su lado
            if alumno[3] == "R":
                problem.addConstraint(movilidad_solo , (alumno[0], alumno2[0]))
            # Si un alumno es conflictivo, el otro es conflictivo o tiene movilidad reducida y además no son hermanos se ejecuta la función que hace que
            # un alumno conflictivo no pueda sentarse al lado de otro
            if alumno[2] == "C" and (alumno2[2] == "C" or alumno2[3] == "R") and alumno[0] != alumno2[4]:
                problem.addConstraint(conflictivo_solo , (alumno[0] , alumno2[0]))
            # Si los 2 alumnos son hermanos y ninguno de los dos tiene movilidad reducida se ejecuta la función que hace que estén juntos
            if alumno[0] == alumno2[4] and alumno[3] != "R" and alumno2[3] != "R":
                problem.addConstraint(hermanos_juntos , (alumno[0] , alumno2[0]))
            # Si un alumno es hermano mayor de otro y ninguno tiene movilidad reducida se ejecuta la función que hace que el mayor esté en el pasillo
            if alumno[1] == "2" and alumno[4] == alumno2[0] and alumno2[1] == "1":
                if alumno[3] != "R" and alumno2[3] != "R":
                    problem.addConstraint(mayor_pasillo, (alumno[0], alumno2[0]))
# Halla todas las soluciones
solucion = problem.getSolutions()
# Crea el archivo de salida para escritura
archivo_salida = open (path + ".output" , "w")
# Escribe el número de soluciones
archivo_salida.write("Numero de soluciones: " + str(len(solucion)) + "\n")

def editar_dic (dic):
    # Esta funcion deja el diccionario como nos lo piden en el enuciado
    dicc_completo = {}
    for clave , valor in dic.items():
        # Se busca al alumno en la tabla de alumnos donde estan todos sus parametros
        dicc_completo[encontrar_alum(clave)] = valor
    
    # Se ordena el diccionario segun el asiento que tenga asignado
    pares = dicc_completo.items()
    pares_ordenados = sorted(pares, key=lambda x: x[1])
    diccionario_ordenado = dict(pares_ordenados)
    return diccionario_ordenado

def encontrar_alum(id):
    # Funcion que busca un alumno y devuelve un str con las caracteristicas del mismo
    for alumno in alumnos:
        if alumno[0] == id:
            return str(alumno[0]) + str(alumno[2]) + str(alumno[3])

if len(solucion) > 3:
    # Obtenemos 3 numeros aleatorios para obtener 3 soluciones aleatorias
    numero1 = random.randint(0, len(solucion) - 1)
    numero2 = random.randint(0, len(solucion) - 1)
    numero3 = random.randint(0, len(solucion) - 1)
    while numero1 == numero2 or numero1 == numero3 or numero2 == numero3:
        # Si dos o más números son iguales, se generan de nuevo
        numero1 = random.randint(0, len(solucion) - 1)
        numero2 = random.randint(0, len(solucion) - 1)
        numero3 = random.randint(0, len(solucion) - 1)
    # Cuando ya tenemos 3 numeros aleatorios distintos, cogemos esas 3 soluciones
    sol1 = solucion[numero1]
    sol2 = solucion[numero2]
    sol3 = solucion[numero3]
    # Convertimos el diccionario a como dice el enuciado y lo escribimos en el archivo de salida
    archivo_salida.write(str(editar_dic(sol1)) + "\n")
    archivo_salida.write(str(editar_dic(sol2)) + "\n")
    archivo_salida.write(str(editar_dic(sol3)))

else:
    # Si hay menos de 3 soluciones , escribirá todas las solucines
    long = len(solucion)
    for i in range(long):
        # Escribimos la solucion en el archivo de salida
        archivo_salida.write(str(editar_dic(solucion[i])) + "\n")

