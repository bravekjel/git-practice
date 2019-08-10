import telepot
from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT= 465
SMTP_USER='wjddpf'
SMTP_PASSWORD ='asd1234'

def send_mail(addr,title, contents):
    msg = MIMEMultipart('alternative')
    msg['From'] = SMTP_USER +'@naver.com'
    msg['To'] = addr
    msg['Subject'] = title

    text = MIMEText(_text=contents, _subtype='html', _charset='utf-8')
    msg.attach(text)

    import smtplib
    smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    smtp.login(SMTP_USER,SMTP_PASSWORD)
    smtp.sendmail(SMTP_USER+'@naver.com', addr, msg.as_string())
    smtp.close()
    
def send_telegram(msg):
    bot = telepot.Bot(settings.TELEGRAM_BOT_ID)
    bot.sendMessage(settings.TELEGRAM_MY_ID,msg)

if __name__ == '__main__':
    send_mail('wjddpf@naver.com','제목','내용')