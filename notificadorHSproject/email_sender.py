import smtplib
from email.mime.text import MIMEText
from notificadorHSproject import app


def activate_mail(email, link):
    sender_email = app.config['MAIL_DEFAULT_SENDER']
    password = app.config['MAIL_PASSWORD']

    message = f"Clique <a href={link}>aqui</a> para confirmar seu email. "


    msg = MIMEText(message, 'html')
    msg['Subject'] = "Validação de seu cadastro no n0t1f1c4d0r HungSing"
    msg['From'] = sender_email
    msg['To'] = email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")
    server.sendmail(sender_email, email, msg.as_string())
    print("Email has been sent to", email)
    server.quit()


def send_mail(username, email, user_pass):
    sender_email = app.config['MAIL_DEFAULT_SENDER']
    password = app.config['MAIL_PASSWORD']

    message = f"<h3>Registro cadastrado</h3><ul><li>Usuario: {username} cadastradx com sucesso</li><li>Senha:{user_pass}</li></ul>"
    # spaced_message = message.replace("\xe1", " ")

    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Bem vindo ao notificador Hung Sing'
    msg['From'] = sender_email
    msg['To'] = email

    # Send email:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")
    server.sendmail(sender_email, email, msg.as_string())
    print("Email has been sent to", email)
    server.quit()
