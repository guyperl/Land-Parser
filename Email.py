import smtplib
import email

session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login('landparsertest@gmail.com', 'Tester#123')

session.sendmail('landparsertest@gmail.com', 'jeffreyxu2008@yahoo.com', 'Test')
session.quit()

print('Mail Sent')
