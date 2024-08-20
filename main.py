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
