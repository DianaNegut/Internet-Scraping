import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

my_email = 'preturi.alerta@gmail.com'
my_password = '*****'

to_email = 'negut.dianamihaela@gmail.com'

msg = MIMEMultipart()
msg['From'] = my_email
msg['To'] = to_email
msg['Subject'] = 'Salut!'

body = 'email de test'
msg.attach(MIMEText(body, 'plain'))

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() 
    server.login(my_email, my_password)
    
    
    text = msg.as_string()
    server.sendmail(my_email, to_email, text)
    print('Email trimis cu succes!')
    
except Exception as e:
    print(f'Eroare la trimiterea email-ului: {e}')

finally:
    server.quit()
