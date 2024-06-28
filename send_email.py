import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email):
    # Detalii despre contul de email (actualizează cu detaliile tale)
    my_email = 'preturi.alerta@gmail.com'
    my_password = 'twcj qmgg ourc ncdh'

    # Creare mesaj
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = to_email
    msg['Subject'] = 'Alertă preț scăzut!'

    # Corpul mesajului
    body = 'Bună! Prețul produsului tău preferat a scăzut sub valoarea țintă pe care ai setat-o.'
    msg.attach(MIMEText(body, 'plain'))

    # Conectare la serverul SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Activare TLS pentru securitate
        server.login(my_email, my_password)
        
        # Trimitere email
        text = msg.as_string()
        server.sendmail(my_email, to_email, text)
        print('Email trimis cu succes!')
        
    except Exception as e:
        print(f'Eroare la trimiterea email-ului: {e}')
        
    finally:
        server.quit()
