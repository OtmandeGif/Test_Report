import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
smtp_server = 'smtp.gmail.com'
port = 465

##Enter version number here (ex : 3.8.15.5.7, 1.2.2 (1), etc..)
Version_number='1.3.5 (1624012175)'

destinataires=['ohassani@urgotech.fr']
for destinataire in destinataires :
    destinateur = 'ohassani.urgo@gmail.com'
    password = 'Testtest123!'
    nom_fichier = 'Report.pdf'
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Bilan des tests de la version '+Version_number
    message['From'] = destinateur
    message['To'] = destinataire
    message.attach(MIMEText('Hello, \n\n Suite aux tests, vous trouverez ci-joint le rapport de test de la version '+Version_number+'. \n\n Bonne aprem ! \n\n Otman', 'plain'))
    with open(nom_fichier, 'rb') as attachment:
        file_part = MIMEBase('application', 'octet-stream')
        file_part.set_payload(attachment.read())
        encoders.encode_base64(file_part)
        file_part.add_header(
        'Content-Disposition',
        'attachment; filename='+ str(nom_fichier)
        )
        message.attach(file_part)
        context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(destinateur, password)
        server.sendmail(destinateur, destinataire, message.as_string())
