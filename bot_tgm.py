"""
    BOT DE TELEGRAM
        Se creó como objetivo de poder consultar rapidamente desde cualquier lugar los .log que 
        produce la aplicación simplemente añadiendo en telegram "BotErrorSalidaMicros"
        Los comandos son /star --> inicia modo comando
                         /help --> muestra los dos comandos para consultar los log.
                         /bd.log --> muestra el log con los errores de conexión a la bd para simular este error borrar ruta relativa "micros.bd" linea 71
                         /crud.log --> detalla los estados de los comandos CRUD del programa
        Este modulo se encuentra como un servicio en el servidor.
"""
import telebot
from observador import ErrorBaseDeDatosObservador


TOKEN = "6671048689:AAFcqQyU0SEeRWSsgMA3WY9zTQSFWHxtcVA"
bot = telebot.TeleBot(TOKEN)
observador = ErrorBaseDeDatosObservador(TOKEN, chat_id="6671048689")

# Creacion comandos simples

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Hola, por favor ingresar /help")

@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(message, "Ingrese /bd.log para ver errores de conexion \n Ingrese /crud.log para ver los enventos CRUD")
    
@bot.message_handler(commands=["bd.log"])
def send_log(message):
    try:
        with open("log_bd.txt", "r") as log_file:
            errors = log_file.read()
            if errors:
                bot.reply_to(message, f"Los errores registrados son:\n\n{errors}")
            else:
                bot.reply_to(message, "No hay errores registrados.")
    except FileNotFoundError:
        bot.reply_to(message, "El archivo de registro no existe.")  

@bot.message_handler(commands=["crud.log"])
def send_log(message):
    try:
        with open("detalles_crud.txt", "r") as log_file:
            errors = log_file.read()
            if errors:
                bot.reply_to(message, f"Eventos de CRUD:\n\n{errors}")
            else:
                bot.reply_to(message, "No hay eventos.")
    except FileNotFoundError:
        bot.reply_to(message, "El archivo de registro de CRUD no existe.")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.polling(none_stop=True)