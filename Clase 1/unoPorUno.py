import unicodedata

# ==== Función para normalizar texto ====
def quitar_tildes(texto):
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto

# ======== PARTE 1 ========

def registro_datos():
    nombre = input("Ingrese su nombre: ")
    edad = int(input("Ingrese su edad: "))
    estatura = float(input("Ingrese su estatura en metros: "))
    print(f"Hola {nombre}, tienes {edad} años y mides {estatura} metros.")
