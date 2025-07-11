import re #se importa para poder usar regular expressions para crear una funcion para crear ruts
import json #se importa json para guardar cuentas
from datetime import datetime

accounts = {}  #Diccionario de cuentas

def guardar(nombre_archivo="cuentas.json"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(accounts, archivo, indent=4)

def cargar(nombre_archivo="cuentas.json"):
    global accounts
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            accounts = json.load(archivo)

        for rut_data in accounts.values():
            for cuenta in rut_data["accounts"].values():
                if "movimientos" not in cuenta:
                    cuenta["movimientos"] = []

    except FileNotFoundError:
        print("No se encontró el archivo de cuentas. Se iniciará con datos vacíos.")

def registrar_movimiento(rut, cuenta, tipo, monto, detalle=""):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    movimiento = {
        "tipo": tipo,
        "monto": monto,
        "fecha": fecha,
        "detalle": detalle
    }
    accounts[rut]["accounts"][cuenta]["movimientos"].append(movimiento)

# 1. Función Login de usuarios
def login(rut):
    '''Lógica de la Función'''
    inserted_RUT = rut
    correct_password = accounts.get(inserted_RUT, {}).get("password")
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        inserted_Password = input("Porfavor ingrese su clave de 4 digitos: ")

        if inserted_RUT in accounts:
            correct_password = accounts[inserted_RUT]["password"]
            if inserted_Password == correct_password:
                print("Has ingresado a tu cuenta.")
                break

            else:
                attempts +=1
                print(f"Clave incorrecta. Tiene {max_attempts - attempts} intentos restantes.")

    if attempts == max_attempts:
        print("Número de intentos alcanzado. Regresando al menú principal.")
        return()


    print("Bienvenido " + inserted_RUT)
    corriente_balance = accounts[inserted_RUT]["accounts"]["corriente"]["balance"]
    vista_balance = accounts[inserted_RUT]["accounts"]["vista"]["balance"] #saldos
    ahorro_balance = accounts[inserted_RUT]["accounts"]["ahorro"]["balance"]
    saldo_total = corriente_balance + vista_balance + ahorro_balance
    print("Saldo total: " + str(saldo_total) + (" CLP."))
    logins = ("1. Consulta de saldos.\n2. Realizar un deposito.\n3. Realizar un retiro.\n4. Realizar transferencia entre cuentas propias.\n5. Realizar transferencia a otro usuario.\n6. Consulta de movimientos. \n7. Volver al menu anterior.")

    while True:
        print(logins)
        opt = input("Por favor seleccione una opción (1, 2, 3, 4, 5, 6, 7): ") #comienzo de opciones en login

        if opt in ["1", "2", "3", "4", "5", "6", "7"]:
            option = int(opt)

            if option == 1: #Consulta de Saldos
                print("Cuenta corriente " + str(corriente_balance) + (" CLP."))
                print("Cuenta vista " + str(vista_balance) + (" CLP."))
                print("Cuenta ahorro " + str(ahorro_balance) + (" CLP."))
                print("Saldo total: " + str(saldo_total) + (" CLP."))
            elif option == 2: #Depositos
                print ("1. Corriente.\n2. Ahorro.\n3. Vista.")
                while True:
                    tipo_Cuenta = input("Por favor seleccione el tipo de cuenta que desea depositar: ")
                    if tipo_Cuenta in ["1", "2", "3"]:
                        if tipo_Cuenta == "1":
                            tipo_Cuenta = "corriente"
                        elif tipo_Cuenta == "2":
                            tipo_Cuenta = "ahorro"
                        else:
                            tipo_Cuenta = "vista"
                        deposit(inserted_RUT, tipo_Cuenta) #se llama a deposit(rut, account_type)
                        corriente_balance = accounts[inserted_RUT]["accounts"]["corriente"]["balance"]
                        vista_balance = accounts[inserted_RUT]["accounts"]["vista"]["balance"]
                        ahorro_balance = accounts[inserted_RUT]["accounts"]["ahorro"]["balance"]
                        saldo_total = corriente_balance + vista_balance + ahorro_balance  #se actualiza balance
                        break
                    else:
                        print("Opción inválida. Intente de nuevo")
            elif option == 3: #Retiros
                print ("1. Corriente.\n2. Ahorro.\n3. Vista.")
                while True:
                    tipo_Cuenta = input("Por favor seleccione el tipo de cuenta que desea retirar: ")
                    if tipo_Cuenta in ["1", "2", "3"]:
                        if tipo_Cuenta == "1":
                            tipo_Cuenta = "corriente"
                        elif tipo_Cuenta == "2":
                            tipo_Cuenta = "ahorro"
                        else:
                            tipo_Cuenta = "vista"
                        withdraw(inserted_RUT, tipo_Cuenta) #se llama a deposit(rut, account_type)
                        corriente_balance = accounts[inserted_RUT]["accounts"]["corriente"]["balance"]
                        vista_balance = accounts[inserted_RUT]["accounts"]["vista"]["balance"]
                        ahorro_balance = accounts[inserted_RUT]["accounts"]["ahorro"]["balance"]
                        saldo_total = corriente_balance + vista_balance + ahorro_balance  #se actualiza balance
                        break
            elif option == 4: #Transferencia propia
                print("Seleccione la cuenta de origen:")
                print("1. Corriente\n2. Ahorro\n3. Vista")
                origen = input("Cuenta origen: ")

                print("Seleccione la cuenta de destino:")
                print("1. Corriente\n2. Ahorro\n3. Vista")
                destino = input("Cuenta destino: ")

                cuentas = {"1": "corriente", "2": "ahorro", "3": "vista"}

                if origen in cuentas and destino in cuentas:
                    origen = cuentas[origen]
                    destino = cuentas[destino]

                    if origen == destino:
                        print("No puede transferir a la misma cuenta.")
                    else:
                        try:
                            monto = float(input("Ingrese el monto a transferir: "))
                            if monto <= 0:
                                print("El monto debe ser mayor que cero.")
                            elif monto > accounts[rut]["accounts"][origen]["balance"]:
                                print("Saldo insuficiente.")
                            else:
                                accounts[rut]["accounts"][origen]["balance"] -= monto
                                accounts[rut]["accounts"][destino]["balance"] += monto
                                print(f"Transferencia exitosa de {monto} CLP desde {origen} a {destino}.")
                                registrar_movimiento(rut, origen, "retiro", monto, f"Transferencia a cuenta {destino}")
                                registrar_movimiento(rut, destino, "depósito", monto, f"Transferencia desde cuenta {origen}")
                                guardar()
                        except ValueError:
                            print("Monto inválido.")
                else:
                    print("Opción inválida.")

                corriente_balance = accounts[inserted_RUT]["accounts"]["corriente"]["balance"]
                vista_balance = accounts[inserted_RUT]["accounts"]["vista"]["balance"]
                ahorro_balance = accounts[inserted_RUT]["accounts"]["ahorro"]["balance"]
                saldo_total = corriente_balance + vista_balance + ahorro_balance

            elif option == 5: #Transferencias entre usuarios

                print("Seleccione la cuenta de origen:")
                print("1. Corriente\n2. Ahorro\n3. Vista")
                origen = input("Cuenta origen: ")
                cuentas = {"1": "corriente", "2": "ahorro", "3": "vista"}

                if origen in cuentas:
                    origen = cuentas[origen]
                    destino_rut = input("Ingrese el RUT del destinatario (sin puntos, con guión): ")

                    if destino_rut == rut:
                        print("No puede transferirse a sí mismo.")
                    elif destino_rut not in accounts:
                        print("El RUT ingresado no existe.")
                    else:
                        print("Seleccione la cuenta destino del otro usuario:")
                        print("1. Corriente\n2. Ahorro\n3. Vista")
                        destino = input("Cuenta destino: ")

                        if destino in cuentas:
                            destino = cuentas[destino]
                            try:
                                monto = float(input("Ingrese el monto a transferir: "))
                                if monto <= 0:
                                    print("El monto debe ser mayor que cero.")
                                elif monto > accounts[rut]["accounts"][origen]["balance"]:
                                    print("Saldo insuficiente.")
                                else:
                                    accounts[rut]["accounts"][origen]["balance"] -= monto
                                    accounts[destino_rut]["accounts"][destino]["balance"] += monto
                                    print(f"Transferencia exitosa de {monto} CLP desde tu cuenta {origen} a la cuenta {destino} del usuario {destino_rut}.")
                                    registrar_movimiento(rut, origen, "retiro", monto, f"Transferencia a usuario {destino_rut}, cuenta {destino}")
                                    registrar_movimiento(destino_rut, destino, "depósito", monto, f"Transferencia desde usuario {rut}, cuenta {origen}")
                                    guardar()
                            except ValueError:
                                print("Monto inválido.")
                        else:
                            print("Cuenta destino inválida.")
                else:
                    print("Cuenta origen inválida.")

                corriente_balance = accounts[inserted_RUT]["accounts"]["corriente"]["balance"]
                vista_balance = accounts[inserted_RUT]["accounts"]["vista"]["balance"]
                ahorro_balance = accounts[inserted_RUT]["accounts"]["ahorro"]["balance"]
                saldo_total = corriente_balance + vista_balance + ahorro_balance

            elif option == 6: #Consulta de movimientos
                print("Seleccione la cuenta para ver movimientos:")
                print("1. Corriente\n2. Ahorro\n3. Vista")
                cuenta = input("Cuenta: ")

                cuentas = {"1": "corriente", "2": "ahorro", "3": "vista"}
                if cuenta in cuentas:
                    cuenta = cuentas[cuenta]
                    movimientos = accounts[inserted_RUT]["accounts"][cuenta].get("movimientos", [])

                    if movimientos:
                        print(f"\nMovimientos de la cuenta {cuenta}:")
                        for i, mov in enumerate(movimientos, 1):
                            print(f"{i}. {mov['fecha']} | {mov['tipo'].capitalize()} | {mov['monto']} CLP | {mov.get('detalle', '')}")
                    else:
                        print(f"No hay movimientos registrados en la cuenta {cuenta}.")
                else:
                    print("Cuenta inválida.")

            else:
                break #break
        else:
            print("Opción inválida. Intente de nuevo")

def create_account():

    rut = input("Favor ingresar su nuevo RUT, sin puntos y con guion: ")
    if validar_rut(rut):
        if rut not in accounts: #se revisa si el rut  ya no esta creado
            while True:
                password = input("Favor ingresar una contraseña de 4 numeros: ")
                if len(password) == 4 and password.isdigit():
                    break
                else:
                    print("La contraseña debe contener exactamente 4 números. Intente de nuevo.")
            accounts[rut] = {
                "password": password,
                "accounts": {
                    "corriente": {"balance": 0, "movimientos": []},
                    "vista": {"balance": 0, "movimientos": []},
                    "ahorro": {"balance": 0, "movimientos": []}
                }
            }
            print("Cuenta creada exitosamente. Bienvenido.") #se crea cuenta
            guardar()
        else:
            print("El RUT ya existe en el sistema.")
    else:
        print("RUT no válido. Favor vuelva a intentar respetando el formato indicado.")

# 2. Función Deposito de Dinero
def deposit(rut, account_type):
    ''' Lógica de la Función '''
    if rut in accounts:
        if account_type in accounts[rut]["accounts"]: #se buca la cuenta a depositar
            try:
                deposit_amount = float(input(f"Ingrese el monto a depositar en la cuenta {account_type}: "))
                if deposit_amount > 0:
                    accounts[rut]["accounts"][account_type]["balance"] += deposit_amount #se compara que el deposito es mayor a 0
                    print(f"Depósito exitoso en la cuenta {account_type}.")
                    registrar_movimiento(rut, account_type, "depósito", deposit_amount)
                    guardar()
                else:
                    print("El monto del depósito debe ser mayor que cero. Vuelva a intentar")
            except ValueError:
                print("Porfavor ingrese un monto válido. Vuelva a intentar")

# 3. Función Retiro de Dinero
def withdraw(rut, account_type):
    ''' Lógica de la Función '''
    if rut in accounts:
        if account_type in accounts[rut]["accounts"]: #se busca la cuenta a retirar
            try:
                withdraw_amount = float(input(f"Ingrese el monto a retirar en la cuenta {account_type}: "))
                if withdraw_amount <= accounts[rut]["accounts"][account_type]["balance"]:
                    accounts[rut]["accounts"][account_type]["balance"] -= withdraw_amount #se comapra si el valor es igual o menor al saldo
                    print(f"Retiro exitoso en la cuenta {account_type}.")
                    registrar_movimiento(rut, account_type, "retiro", withdraw_amount)
                    guardar()
                else:
                    print("Saldo insuficiente. Vuelva a intentar")
            except ValueError:
                print("Porfavor ingrese un monto válido. Vuelva a intentar")

# 4. Función Menú Principal
def main():
    ''' Lógica del Menú '''
    print("Bienvenido al Cajero ATM de 'PyTrustBank International'")
    print("Seleccione el numero indicando la accion que necesita realizar:")
    Saludo = ("1. Iniciar Sesion.\n2. Crear una cuenta.\n3. Salir.")
    while True:
        print(Saludo)
        opt = input("Por favor seleccione una opción (1, 2, o 3): ")

        if opt in ['1', '2', '3']: #Primeras opciones
            option = int(opt)

            if option == 1:
                rut = input("Favor ingresar su RUT, sin puntos y con guion: ")
                if rut in accounts:
                    login(rut) #se ingresa al menu de login
                else:
                    print("RUT no encontrado. Vuelva a intentar.")
            elif option == 2:
                create_account()
            else:
                print("Gracias por preferirnos, nos vemos.") #salir
                break
        else:
            print("Opción inválida. Intente de nuevo")

def validar_rut(rut): #se crea para forzar el segmento de un rut chileno al crear cuenta.

    rut_Valido = r'^\d{7,8}-[0-9Kk]$'

    # Use the re.match() function to check if the RUT matches the pattern
    if re.match(rut_Valido, rut):
        return True
    else:
        return False

# 5. Llamada de la Función Principal al ejecutar el Script

if __name__ == "__main__":
    cargar()   # ← esto carga el archivo si existe
    main()     # ← inicia el cajero


