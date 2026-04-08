import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def enviar_reporte(destinatario: str, pdf_path: str):
    remitente = os.environ.get("EMAIL_REMITENTE")
    password  = os.environ.get("EMAIL_PASSWORD")

    if not remitente or not password:
        raise ValueError(
            "Faltan variables de entorno EMAIL_REMITENTE y/o EMAIL_PASSWORD. "
            "Revisá el archivo .env"
        )

    msg            = MIMEMultipart()
    msg["From"]    = remitente
    msg["To"]      = destinatario
    msg["Subject"] = "Reporte mensual de ventas — Ferretería Don José"

    cuerpo = """\
Hola,

Adjunto encontrás el reporte automático de ventas del mes.
Fue generado automáticamente con Python a partir del registro de ventas.

Saludos.
"""
    msg.attach(MIMEText(cuerpo, "plain"))

    with open(pdf_path, "rb") as f:
        adjunto = MIMEBase("application", "octet-stream")
        adjunto.set_payload(f.read())

    encoders.encode_base64(adjunto)
    adjunto.add_header(
        "Content-Disposition",
        f"attachment; filename={os.path.basename(pdf_path)}"
    )
    msg.attach(adjunto)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remitente, password)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        print(f"  ✓ Reporte enviado a {destinatario}")


if __name__ == "__main__":
    # Prueba rápida: python emailer.py destino@gmail.com
    import sys
    if len(sys.argv) < 2:
        print("  Uso: python emailer.py destinatario@email.com")
        sys.exit(1)
    from dotenv import load_dotenv
    load_dotenv()
    enviar_reporte(sys.argv[1], "output/reporte_ventas.pdf")
