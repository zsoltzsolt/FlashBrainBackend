import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(receiver_email, subject, message_body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  
    
    sender_email = "zsoltzsolt303@gmail.com"  
    sender_password = "ukhr jrny uehq mxzj"

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  

    server.login(sender_email, sender_password)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach the HTML-formatted message
    msg.attach(MIMEText(message_body, "html"))

    server.sendmail(sender_email, receiver_email, msg.as_string())

    server.quit()
