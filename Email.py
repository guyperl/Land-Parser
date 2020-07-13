import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import getpass


def get_email_parameters():
    sender = input('Input login: ')
    password = getpass.getpass('Input password: ')
    receiver = input('Input receiver: ')
    files = input('Enter file name: ')

    return sender, password, receiver, files


def send_mail(send_from, password, send_to, files=None):
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(send_from, password)

    text = ''

    with open(files, 'r') as file:
        text = file.read()

    session.sendmail(send_from, send_to, text)
    session.quit()


def main():
    sender, password, receiver, files = get_email_parameters()
    send_mail(sender, password, receiver, files)


if __name__ == '__main__':
    main()


print('Email sent')

