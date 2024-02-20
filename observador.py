"""
Modulo observador se utiliza para monitorizar los eventos de conexión a la base de datos como asi
reportar tanto en consola como en log.txt
Se utiliza el modulo telebot para que pueda comunicarse con el modulo bot_tgm.py
"""


from datetime import datetime
import telebot

class Observador:
    def on_error(self, mensaje):
        pass


class ErrorBaseDeDatosObservador(Observador):
    def __init__(self, log_path="log_bd.txt", token=None, chat_id=None):
        self.log_path = log_path
        self.token = token
        self.chat_id = chat_id
        self.bot = telebot.TeleBot(token) if token else None

    def on_error(self, mensaje):
        print(f"Error en la base de datos: {mensaje}")
        self.guardar_log(f"Error en la conexion a la base de datos: {mensaje}: {datetime.now()}")
        self.enviar_mensaje_telegram(f"Error en la conexion a la base de datos: {mensaje}: {datetime.now()}")

    def guardar_log(self, mensaje):
        with open(self.log_path, "a") as log_file:
            log_file.write(f"{mensaje}\n")

    def enviar_mensaje_telegram(self, mensaje, error_message=None):
        if self.bot and self.chat_id:
            if error_message:
                mensaje += f"\n\nError registrado: {error_message}"
            self.bot.send_message(chat_id=self.chat_id, text=mensaje)

