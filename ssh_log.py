"""
Modulo que contiene la configuración y los comandos necesarios usando la libreria de paramiko
para enviar los log hacia el servidor virtualizado sobre AWS.
Este modulo se utiliza cuando el programa advierte algún error de conexión a la BD como cuando 
se sale del programa, para guardar los eventos de crud.
"""

import paramiko


def transferir_archivos_scp(archivos_locales, archivos_remotos, servidor, puerto, usuario, clave_privada=None, clave_passphrase=None):
    # Crear una instancia de cliente SSH
    ssh_client = paramiko.SSHClient()

    try:
        # Configurar el cliente SSH
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar al servidor SSH
        if clave_privada:
            private_key = paramiko.RSAKey.from_private_key_file(clave_privada, password=clave_passphrase)
            ssh_client.connect(servidor, port=puerto, username=usuario, pkey=private_key)
        else:
            ssh_client.connect(servidor, port=puerto, username=usuario, password=clave_passphrase)

        # Crear un canal SFTP
        sftp = ssh_client.open_sftp()

        # Transferir cada archivo local al servidor remoto
        for archivo_local, archivo_remoto in zip(archivos_locales, archivos_remotos):
            sftp.put(archivo_local, archivo_remoto)
            print(f"Archivo {archivo_local} transferido exitosamente a {servidor}:{archivo_remoto}")

        # Cerrar el canal SFTP y la conexión SSH
        sftp.close()
        ssh_client.close()

    except Exception as e:
        print(f"Error al transferir los archivos: {e}")


def transferir_archivos_on_error(archivos_locales, archivos_remotos):
    # Configuración de conexión SSH
    servidor = "ec2-54-94-182-241.sa-east-1.compute.amazonaws.com"
    puerto = 22  # Puerto SSH por defecto
    usuario = "Administrator"
    clave_privada = ""  # Ruta a tu clave privada (si utilizas autenticación por clave privada)
    clave_passphrase = "kxSmuk8ujQ0umGUScJWb2W3W!yftiFBS"  # Contraseña de tu clave privada (si está encriptada)

    # Transferir los archivos por SSH
    transferir_archivos_scp(archivos_locales, archivos_remotos, servidor, puerto, usuario, clave_privada, clave_passphrase)
