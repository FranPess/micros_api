"""
Controlador: Es el encargado de  lanzar la aplicación
Importa los siguientes:
* Librería Tkinter
* Modulo vista: Encargado de generar la vista
* Modulo Modelo: Encargo de ejecutar las funciones
"""
from tkinter import Tk
from vista import Ventana
from modelo import Modelo
from observador import ErrorBaseDeDatosObservador


if __name__ == "__main__":
    
    token = "AAFcqQyU0SEeRWSsgMA3WY9zTQSFWHxtcVA"
    chat_id = "6671048689"
    
    modelo = Modelo()
    observador = ErrorBaseDeDatosObservador(token=token, chat_id=chat_id)  # Configura el observador con token y chat ID

    root_tk = Tk()
    ventana_micros = Ventana(root_tk, modelo)
    root_tk.geometry("1280x720")
    root_tk.resizable(True, True)   #Permite que la ventana sea re-dimensionable
    root_tk.mainloop()
