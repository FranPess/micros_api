"""
Modelo: Módulo que contiene la clase Modelo
Dentro de esta clase se encuentran contenidas todos los métodos que permiten:

* cargar los datos a la aplicación
* Borrar datos de la aplicación
* Manipular datos de la aplicación
* Actualizar hora
"""

import re
import os
import sys
import atexit
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk, END
from conex_bd import ConexionBD
from os.path import abspath, dirname, join
from functools import wraps
from ssh_log import transferir_archivos_on_error

"""
Se importa:
* Librería Tkinter
* Librería Datetime
* Módulo conex_bd (Encargado de manejar las bases de datos)
* librería os.path
"""

def log_crud(func):
    @wraps(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            resultado = func(*args, **kwargs)
            with open("detalles_crud.txt", "a") as file:
                file.write(f"Operación {func.__name__}: {datetime.now()} - Exito\n")
            return resultado
        except Exception as e:
            with open("detalles_crud.txt", "a") as file:
                file.write(f"Operación {func.__name__}: {datetime.now()} - Error: {str(e)}\n")
            raise   
    return wrapper
    

class Modelo:
    """ Clase Módelo"""
    def __init__(self):                             #Constructor
        """
        * script_dir: Variable que contiene la dirección del archivo
        * db_ruta: Variable que contiene la ruta a la base de datos
        * self.bd: objeto de la clase ConexionBD
        * conex():función del modulo conex_bd. Obtiene la ruta e intenta conectarse con la base de datos
        """
        script_dir = dirname(abspath(__file__))     # Se obtiene la ruta del archivo
        db_ruta = join(script_dir, "micros.db")     # Se obtiene la  ruta de la base de datos
        self.bd = ConexionBD(db_ruta)               #Objeto de la clase  ConexionBD
        self.bd.conex()
    # Validaciones regex, CRUD
    def validar_campo(self, interno, numero, chofer, recorrido, salida):
        """
        Método de validación de campos:
        * interno: interno del colectivo
        * número: Número del recorrido
        * recorrido: nombre del recorrido
        * salida: Hora de salida
        """
        if (interno == "") or (numero == "") or (chofer == "") or (
                recorrido == "") or (salida == ""):
            messagebox.showwarning(title="Error", message="Revise sus datos de entrada")
        else:
            return True
    @log_crud
    def alta(self, entrada1, entrada2, entrada3, entrada4, entrada5, tree):
        """
        Método alta: Este método de la clase tiene la función de tomar los valores cargados en la ventana
        y subirlos a la base de datos. Previo a esto realiza una serie de comprobaciones para asegurarse 
        de que los datos estan bien cargados, si no se ha dejado ningún campo vacíos o si los datos cargados
        estan repetidos.

        * entrada1: interno del colectivo
        * entrada2: Número del recorrido
        * entrada3: nombre del recorrido
        * entrada4: Hora de salida
        * entrada5: Fecha
        * tree: Variable del treeview
        """
        global fecha
        fecha = datetime.now().strftime('%d/%m/%Y')
        #Se validan los campos a travez del metodo validar_campos()
        if self.validar_campo(entrada1.get(), entrada2.get(), entrada3.get(), entrada4.get(), entrada5.get()):
            validar = entrada5.get()
            patron = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
            if re.match(patron, validar):       #Se valida el patron 
                try:
                    self.bd.conectar()
                    for item in tree.get_children():
                        #se comparan los datos introducidos con los existentes en busca de que sean repetidos
                        if (entrada1.get(), entrada2.get(), entrada3.get(), entrada4.get()) == tuple(
                                tree.item(item, "values"))[:4]:
                            messagebox.showwarning(title="Error", message="Esta salida ya se encuentra cargada")
                            self.bd.cerrar_conexion()
                            return
                    #Se cargan los datos a guardar en la base de datos
                    data = (entrada1.get(), entrada2.get(), entrada3.get(), entrada4.get(), entrada5.get(), fecha)
                    self.bd.cursor.execute(
                        "INSERT INTO salidas(interno, numero, chofer, recorrido, salida, fecha) VALUES(?, ?, ?, ?, ?,?)",
                        data)
                    self.bd.con.commit()
                    print("Estoy en alta todo ok")
                    self.bd.cerrar_conexion()
                    tree.delete(*tree.get_children())  # Limpiar todos los elementos en el treeview
                    self.actualizar_treeview(tree)  # Volver a cargar los datos en el treeview
                except Exception as e:
                    self.bd.cerrar_conexion()   #Se cierra la conexion de la base de datos
                    print("Error:", str(e))     #Muestra el error en caso de que lo haya
            else:
                messagebox.showwarning(title="Error", message="Ingrese Hora válida")    #Muestra el error en caso de que lo haya

    @log_crud
    def editar(self, entrada1, entrada2, entrada3, entrada4, entrada5, tree):
        """
        Método editar:
        * entrada1: interno del colectivo
        * entrada2: Número del recorrido
        * entrada3: nombre del recorrido
        * entrada4: Hora de salida
        * entrada5:Fecha
        * tree: Variable del treeview
        """
        if self.validar_campo(entrada1.get(), entrada2.get(), entrada3.get(), entrada4.get(), entrada5.get()):
            global item2
            validar = entrada5.get()    #Se toma la hora de salida como patron a comparar
            patron = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
            if re.match(patron, validar):
                id = item2['text']
                if id == (''):
                    messagebox.showwarning(title="Error", message="Seleccionar un ítem para actualizar")
                else:
                    try:    #Intenta guardar los datos en la base de datos, en caso de que no pueda ejecuta la excepcion
                        self.bd.conectar()
                        data = (entrada1.get(), entrada2.get(), entrada3.get(), entrada4.get(), entrada5.get(), id)
                        self.bd.cursor.execute(
                            "UPDATE salidas SET interno=?, numero=?, chofer=?, recorrido=?, salida=? WHERE id=?;",
                            data)
                        self.bd.con.commit()
                        tree.delete(*tree.get_children())  # Limpiar todos los elementos en el treeview
                        self.actualizar_treeview(tree)  # Volver a cargar los datos en el treeview
                        self.bd.cerrar_conexion()
                    except Exception as e:
                        self.bd.cerrar_conexion()
                        print("Error:", str(e))
            else:
                messagebox.showwarning(title="Error", message="Ingresar Hora válida")
                
    @log_crud
    def borrar(self, entrada1, entrada2, entrada3, entrada4, entrada5, tree):
        """
        Método borrar:
        * entrada1: interno del colectivo
        * entrada2: Número del recorrido
        * entrada3: nombre del recorrido
        * entrada4: Hora de salida
        * entrada5: Fecha
        * tree: Variable del treeview
        """
        global item2
        valor = tree.selection()    #Guarda en valor, los datos obtenidos de la seleccion
        if item2 == '':
            messagebox.showwarning(
                title="Error", message="Seleccionar un item para borrar")
        else:
            interno = item2['text']
            try:                    #intenta borrar los datos selecionados
                self.bd.conectar()
                data = (interno,)
                self.bd.cursor.execute("DELETE FROM salidas WHERE id = ?", data)
                self.bd.con.commit()
                tree.delete(valor)
                self.borrar_campo(entrada1, entrada2, entrada3, entrada4, entrada5)
                self.bd.cerrar_conexion()
            except Exception as e:
                self.bd.cerrar_conexion()
                print("Error:", str(e))
    
    # Función actualiza treeview
    
    def actualizar_treeview(self, tree):
        """
        Método actualizar_treeview: actualiza los datos que se encuentran en el treeview
        Este método toma los datos de la base de datos en la variable "datos" y los recorre uno a uno 
        tomando la hora de salida del colectivo  en la variable "hora_salida" y la compara con la hora
        actual mediante una resta y calcula el tiempo que resta para salir. En función de eso imprime 
        los datos en pantalla. Si restan menos de 5 minutos los pinta de color rojo
        * treeview:Variable treeview
        * datos: Variable que contiene los datos de la base de datos
        * tiempo: Variable que contiene la hora actual
        * fecha: Variable que contiene la fecha actual
        * hora_salida: Variable que contiene la hora de salida del colectivo
        * restan: variable que contiene la diferencia entre la hora actual y la salida del colectivo
        * limite:Variable que contiene el tiempo que falta para que salga el colectivo expresados den segundos

        """
        records = tree.get_children()   #obtiene los datos del treeview
        for element in records:         #Borra los datos del treeview
            tree.delete(element)
        # Se guardan datos tiempo y fecha
        tiempo = datetime.now()                     #Variable que mantiene la hora actual
        fecha = datetime.now().strftime('%d/%m/%Y') #Variable que mantiene la fecha actual

        try:                    #Intenta conectarse con la ase de datos
            self.bd.conectar()  #Metodo de la clase ConexionBD que permite conectarse con la base de datos
            self.bd.cursor.execute("SELECT * FROM salidas ORDER BY datetime(salida) DESC")
            datos = self.bd.cursor.fetchall()   #Variable que contiene los datos de la base de datos

            for fila in datos:
                """Se recorren los datos para revisar su hora de salida y en función de eso presentar el 
                    recorrido den pantalla
                """
                hora_salida = datetime.strptime(fecha + " " + fila[5] + ":00", "%d/%m/%Y %H:%M:%S")
                restan = hora_salida - tiempo
                limite = restan.seconds
                # Se compara hora de salida 
                if ((hora_salida > tiempo) and (fecha == fila[6])): 
                    """ Se compara si el horario de salida es mayor a la hora actual lo cual indica que no salido ya
                        Se compara si la fecha actual es igual a la fecha de salida para no publicar  recorridos de días anteriores         
                    """
                    if limite < 300:
                        """ Verifica si el tiempo que resta para que el colectivo salga es menor a 5 minutos, en caso
                            afirmativo lo pinta de color rojo    
                        """
                        style = ttk.Style()
                        style.map('Treeview', background=[('selected', 'blue')])
                        tree.tag_configure('ya_sale', background="red", font=(None, 25))
                        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5]),
                                    tags=('ya_sale',))
                    else:
                        tree.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5]))
                    
            self.bd.cerrar_conexion()
        except Exception as e:
            self.bd.cerrar_conexion()
            print("Error:", str(e))
    
    
    def borrar_campo(self, entrada1, entrada2, entrada3, entrada4, entrada5):
        """
        Método borrar_campo: Este método tiene la función de borrar los campos de la aplicación 
        cada vez que es llamada, de esta forma el usuario visualiza que la acción tuvo a lugar
        * entrada1: interno del colectivo
        * entrada2: Número del recorrido
        * entrada3: nombre del recorrido
        * entrada4: Hora de salida
        * entrada5:Fecha
        
        """
        entrada1.delete(0, END)
        entrada2.delete(0, END)
        entrada3.delete(0, END)
        entrada4.delete(0, END)
        entrada5.delete(0, END)
    # Función selección de salida en treeview
    
    def seleccion(self, e, tree, entrada1, entrada2, entrada3, entrada4, entrada5):
        """
        Metodo seleccion:Este método tiene la función de obtener todos los valores de la selección realizada
        en la ventana de la aplicación
        * entrada1: interno del colectivo
        * entrada2: Número del recorrido
        * entrada3: nombre del recorrido
        * entrada4: Hora de salida
        * entrada5: Fecha
        * tree: Variable del treeview
        * e: Variable del la funcion
        """
        global item2
        valor = tree.selection()
        item2 = tree.item(valor)
        selected = tree.focus()
        self.borrar_campo(entrada1, entrada2, entrada3, entrada4, entrada5) #Se borran los campos de la aplicacion

        #Se genera una lista con los valores seleccionados para luego cargarlos en cada uno de los campos
        values = list(tree.item(selected, 'values'))
        entrada1.insert(0, values[0])
        entrada2.insert(0, values[1])
        entrada3.insert(0, values[2])
        entrada4.insert(0, values[3])
        entrada5.insert(0, values[4])
       
    
    def actualizar_tiempo(self, clock_widget, tiempo_widget):
        """
        Método actualizar_tiempo: Este método tiene la función de actualizar el tiempo en la ventana de
        la aplicación cada vez que es llamado.
        * clock_widget: Label traída desde el módulo vista
        * tiempo_widget: Label traída desde el módulo vista
        """
        date = datetime.now().strftime('%d/%m/%y')
        current_time = datetime.now().strftime('%H:%M:%S')
        clock_widget.config(text=current_time, bg="black", fg="white", font="Kameron 70 bold")
        tiempo_widget.config(text=date, bg="black", fg="white", font="Kameron 30 bold")
    

def enviar_logs_al_salir():
    transferir_archivos_on_error(["log_bd.txt", "detalles_crud.txt"], ["C:/Users/Administrator/Desktop/TGM_Bot/log_bd.txt", "C:/Users/Administrator/Desktop/TGM_Bot/detalles_crud.txt"])
    atexit.register(enviar_logs_al_salir)
    sys.exit()
