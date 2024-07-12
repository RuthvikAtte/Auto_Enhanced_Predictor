import smtplib
from email.mime.text import MIMEText


def send_email(subject, body, to_email):
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
    smtp_port = (
        587  # Replace with your SMTP port (typically 587 for TLS or 465 for SSL)
    )
    from_email = "rutgersnbsniper@gmail.com"  # Replace with your email address
    password = "woff flkn kgyu dwre"  # Replace with your email password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, [to_email], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    import sys

    subject = "Service myapp.service has stopped"
    body = "The myapp.service has stopped running. Please check the server."
    to_email = "ruthvikatte24@gmail.com"  # Replace with the recipient's email address
    send_email(subject, body, to_email)
