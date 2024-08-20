En python, dame un programa que haga lo siguiente:
- Cada vez oprima la combinacion de teclas: CTRL + ALT + A, haga capturas de pantalla completas y
acumule los archivos .png
- Cuando oprima la combinacion de teclas: CTRL + ALT + M, mande todos esos archivos acumulados por 
email, aun email de gmail, y con copia para otro email
- Para los correos electronicos que use las varias de entorno: para el email que sea la variable USER_EMAIL y para el otro en mail cc con copia que use la variable OTHER_EMAIL


Claro, aquí tienes el programa modificado para eliminar todos los archivos `.png` acumulados del directorio actual después de haberlos enviado por correo electrónico.

```python
import smtplib
import ssl
import keyboard
import os
from PIL import ImageGrab
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

screenshot_files = []

def take_screenshot():
    # Captura la pantalla
    screenshot = ImageGrab.grab()
    screenshot_file = f"screenshot_{len(screenshot_files) + 1}.png"
    screenshot.save(screenshot_file)
    screenshot_files.append(screenshot_file)
    print(f"Screenshot saved as {screenshot_file}")

def send_email_with_attachments(to_email, cc_email, subject, body, attachments):
    # Información del correo electrónico y del servidor SMTP
    from_email = os.getenv('USER_EMAIL')
    from_password = os.getenv('USER_PASSWD')
    smtp_server = "smtp.gmail.com"
    port = 587  # Para starttls

    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Cc"] = cc_email
    msg["Subject"] = subject

    # Adjuntar el cuerpo del correo
    msg.attach(MIMEText(body, "plain"))

    # Adjuntar los archivos
    for attachment in attachments:
        part = MIMEBase("application", "octet-stream")
        with open(attachment, "rb") as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment}",
        )
        msg.attach(part)

    # Enviar el correo electrónico
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(from_email, from_password)
        server.sendmail(from_email, [to_email, cc_email], msg.as_string())

    print("Email sent successfully")

def delete_screenshot_files(files):
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

def on_screenshot_hotkey():
    take_screenshot()

def on_send_email_hotkey():
    if screenshot_files:
        send_email_with_attachments(
            os.getenv('USER_EMAIL'),
            os.getenv('OTHER_EMAIL'),
            "Screenshots Captured",
            "Here are the screenshots you requested.",
            screenshot_files
        )
        delete_screenshot_files(screenshot_files)
        screenshot_files.clear()
    else:
        print("No screenshots to send")

# Asignar la combinación de teclas Ctrl + Alt + A para tomar la captura y Ctrl + Alt + M para enviar el correo
keyboard.add_hotkey('ctrl+alt+a', on_screenshot_hotkey)
keyboard.add_hotkey('ctrl+alt+m', on_send_email_hotkey)

# Mantener el script en ejecución
print("Press Ctrl+Alt+A to take a screenshot and Ctrl+Alt+M to send them via email...")
keyboard.wait('esc')  # Usa 'esc' para salir del programa
```

Este programa hace lo siguiente:
1. `take_screenshot` captura la pantalla y guarda la imagen como `screenshot_{n}.png`, donde `{n}` es el número de captura.
2. `send_email_with_attachments` envía un correo electrónico con todos los archivos de captura acumulados como adjuntos.
3. `delete_screenshot_files` elimina todos los archivos de captura después de que el correo ha sido enviado.
4. Usa `keyboard.add_hotkey` para asignar las combinaciones de teclas `Ctrl+Alt+A` para tomar capturas de pantalla y `Ctrl+Alt+M` para enviar las capturas por correo electrónico.

Asegúrate de tener las variables de entorno `USER_EMAIL`, `USER_PASSWD` y `OTHER_EMAIL` configuradas antes de ejecutar el programa. Para ejecutar el programa, simplemente usa:

```sh
python main
.py
```


Para ejecutar el programa en segundo plano, puedes usar diferentes métodos dependiendo del sistema operativo que estés utilizando. Aquí te explico cómo hacerlo en Windows y en sistemas Unix (Linux, macOS).

### Windows

En Windows, puedes ejecutar un script de Python en segundo plano utilizando el siguiente comando en PowerShell:

1. Crea un archivo `run_in_background.ps1` con el siguiente contenido:

    ```powershell
    Start-Process "python" -ArgumentList "tu_programa.py" -WindowStyle Hidden
    ```

2. Ejecuta el archivo `.ps1` desde PowerShell:

    ```powershell
    .\run_in_background.ps1
    ```

Esto ejecutará el script de Python en segundo plano sin mostrar una ventana de consola.

### Unix (Linux, macOS)

En sistemas Unix, puedes ejecutar el script de Python en segundo plano utilizando `nohup` o redirigiendo la salida a `/dev/null`.

1. Abre una terminal y ejecuta el siguiente comando:

    ```sh
    nohup python tu_programa.py &
    ```

   O también puedes redirigir la salida estándar y de error a `/dev/null`:

    ```sh
    python tu_programa.py > /dev/null 2>&1 &
    ```

En ambos casos, el script se ejecutará en segundo plano. El uso de `&` al final del comando indica que el proceso debe ejecutarse en segundo plano.

### Ejemplo Completo para Unix

Si deseas que el script se ejecute al inicio del sistema, puedes agregarlo a `crontab` con la siguiente línea:

1. Edita el crontab:

    ```sh
    crontab -e
    ```

2. Agrega la siguiente línea al final del archivo para ejecutar el script al inicio del sistema:

    ```sh
    @reboot nohup python /ruta/a/tu_programa.py &
    ```

Esto ejecutará el script en segundo plano cada vez que el sistema se reinicie.

### Ejemplo Completo para Windows

Si prefieres hacer que el script se ejecute al inicio del sistema en Windows, puedes agregar un acceso directo al script en la carpeta de inicio:

1. Crea un acceso directo al archivo `run_in_background.ps1`.
2. Copia este acceso directo a la carpeta de inicio. Puedes abrir la carpeta de inicio ejecutando `shell:startup` en la ventana de ejecución (`Win + R`).

Esto hará que el script se ejecute en segundo plano cada vez que inicies sesión en Windows.

Con estos métodos, puedes asegurarte de que tu script se ejecute en segundo plano en diferentes sistemas operativos.

Para traer un proceso de segundo plano a primer plano en Linux, puedes utilizar los comandos `jobs`, `fg`, y `bg`. A continuación, te explico cómo hacerlo.

### Pasos para traer un proceso a primer plano

1. **Ejecutar un comando en segundo plano:**

    Si aún no has enviado el proceso al segundo plano, puedes iniciar un proceso y enviarlo al segundo plano agregando `&` al final del comando:

    ```sh
    some_command &
    ```

2. **Listar los trabajos en segundo plano:**

    Usa el comando `jobs` para listar los trabajos en segundo plano:

    ```sh
    jobs
    ```

    La salida se verá algo así:

    ```sh
    [1]+  Running                 some_command &
    [2]-  Stopped                 another_command
    ```

    Aquí, los números `[1]` y `[2]` son los ID de trabajo (job ID).

3. **Traer un proceso a primer plano:**

    Usa el comando `fg` seguido del ID del trabajo (job ID) para traer el proceso a primer plano. Por ejemplo, para traer el trabajo `[1]` a primer plano:

    ```sh
    fg %1
    ```

    Si solo tienes un trabajo en segundo plano, puedes simplemente usar:

    ```sh
    fg
    ```

4. **Enviar un proceso a segundo plano y traerlo de nuevo a primer plano:**

    Si tienes un proceso en primer plano y quieres enviarlo a segundo plano, puedes suspenderlo temporalmente usando `Ctrl + Z` y luego usar `bg` para reanudarlo en segundo plano:

    - Suspender el proceso actual (en primer plano):

      ```sh
      Ctrl + Z
      ```

    - Reanudar el proceso en segundo plano:

      ```sh
      bg
      ```

    - Traerlo de nuevo a primer plano más tarde:

      ```sh
      fg
      ```

### Ejemplo completo

1. Ejecutar un comando en segundo plano:

    ```sh
    sleep 300 &
    ```

2. Listar los trabajos en segundo plano:

    ```sh
    jobs
    ```

    Salida esperada:

    ```sh
    [1]+  Running                 sleep 300 &
    ```

3. Traer el trabajo `[1]` a primer plano:

    ```sh
    fg %1
    ```

### Nota

- Los comandos `fg` y `bg` funcionan en la misma sesión de terminal desde la que se enviaron los procesos a segundo plano.
- Si cierras la sesión de terminal, los trabajos en segundo plano se terminarán a menos que se utilicen herramientas como `nohup` o `screen` para mantenerlos en ejecución.



$ nohup.exe python main.py &
[1] 1170
nohup: ignoring input and appending output to 'nohup.out'
