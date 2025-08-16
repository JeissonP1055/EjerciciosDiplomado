import unicodedata

# ==== Función para normalizar texto ====
def quitar_tildes(texto):
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

# Lista global para el punto 11
estudiantes = []

# ======== PARTE 1 ========

def registro_datos():
    nombre = input("Ingrese su nombre: ")
    edad = int(input("Ingrese su edad: "))
    estatura = float(input("Ingrese su estatura en metros: "))
    print(f"Hola {nombre}, tienes {edad} años y mides {estatura} metros.")

def calculo_rapido():
    num1 = float(input("Ingrese el primer número: "))
    num2 = float(input("Ingrese el segundo número: "))
    suma = num1 + num2
    resta = num1 - num2
    multiplicacion = num1 * num2
    division = num1 / num2 if num2 != 0 else "Indefinida"
    print(f"Suma: {suma}\nResta: {resta}\nMultiplicación: {multiplicacion}\nDivisión: {division}")



def lista_compras():
    compras = ["Pan", "Leche", "Huevos", "Queso", "Café"]
    print("Primer producto:", compras[0])
    print("Último producto:", compras[-1])
    nuevo = input("Ingrese un nuevo producto: ")
    compras.append(nuevo)
    compras = sorted(compras, key=quitar_tildes)  # Ordena ignorando mayúsculas y tildes
    print("Lista ordenada:", compras)

def notas_estudiante():
    notas = (3.5, 4.0, 2.8, 4.5)
    print("Nota más alta:", max(notas))
    print("Nota más baja:", min(notas))
    promedio = sum(notas) / len(notas)
    print("Promedio:", promedio)

# ======== PARTE 3 ========

def mensaje_bienvenida():
    print("Bienvenido al curso de Python")

def saludar(nombre):
    print(f"Hola {nombre}, ¡bienvenido!")

def calcular_area_rectangulo(base, altura):
    return base * altura

# ======== PARTE 4 ========

def uso_funciones_integradas():
    texto = input("Ingrese un texto: ")
    print("Minúsculas:", texto.lower())
    print("Mayúsculas:", texto.upper())
    print("Título:", texto.title())
    print("Número de caracteres:", len(texto))

def filtrado_numeros():
    numeros = list(range(1, 10))
    pares = list(filter(lambda x: x % 2 == 0, numeros))
    print("Números pares:", pares)

def enumeracion_ciudades():
    ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla"]
    for i, ciudad in enumerate(ciudades, start=1):
        print(f"{i}. {ciudad}")

# ======== PARTE 5 ========

def agregar_estudiante(nombre, edad):
    estudiantes.append((nombre, edad))

def mostrar_estudiantes():
    for nombre, edad in estudiantes:
        print(f"Nombre: {nombre}, Edad: {edad}")

# ======== MENÚ PRINCIPAL ========

while True:
    print("\n--- MENÚ ---")
    print("1. Registro de datos")
    print("2. Cálculo rápido")
    print("3. Lista de compras")
    print("4. Notas de un estudiante")
    print("5. Mensaje de bienvenida (3 veces)")
    print("6. Saludar")
    print("7. Calcular área de un rectángulo")
    print("8. Uso de funciones integradas (texto)")
    print("9. Filtrar números pares")
    print("10. Enumerar ciudades")
    print("11. Mini sistema de estudiantes")
    print("0. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        registro_datos()
    elif opcion == "2":
        calculo_rapido()
    elif opcion == "3":
        lista_compras()
    elif opcion == "4":
        notas_estudiante()
    elif opcion == "5":
        for _ in range(3):
            mensaje_bienvenida()
    elif opcion == "6":
        nombre = input("Ingrese su nombre: ")
        saludar(nombre)
    elif opcion == "7":
        base = float(input("Ingrese la base: "))
        altura = float(input("Ingrese la altura: "))
        print("Área del rectángulo:", calcular_area_rectangulo(base, altura))
    elif opcion == "8":
        uso_funciones_integradas()
    elif opcion == "9":
        filtrado_numeros()
    elif opcion == "10":
        enumeracion_ciudades()
    elif opcion == "11":
        for _ in range(3):
            nombre = input("Nombre del estudiante: ")
            edad = int(input("Edad: "))
            agregar_estudiante(nombre, edad)
        print("Listado de estudiantes:")
        mostrar_estudiantes()
    elif opcion == "0":
        print("Saliendo del programa...")
        break
    else:
        print("Opción inválida.")
