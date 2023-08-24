import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from jinja2 import Environment, FileSystemLoader, select_autoescape

from pyqrcode import create
import io
import base64


def send_mail():
    env = Environment(
        loader=FileSystemLoader('email_templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template("message.html") # 模板文件
    email_user = ""  # 发件人
    fake_user = formataddr(["人力资源部", ""]) # 发件人伪造

    password = ""  # 邮箱密码
    subject = ""  # 主题

    with open('test.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for line in reader:
            # 根据模板生成html邮件
            html = template.render(qrcode_b64=gen_qrcode(line[2]))
            # print(html)
            email_send = line[1]
            msg = MIMEMultipart("alternative")
            # msg['From'] = email_user
            msg['From'] = fake_user
            msg['To'] = email_send
            msg['Subject'] = subject
            msg.attach(MIMEText(html, "html"))

            server = smtplib.SMTP_SSL("smtp.example.com", 465) # 邮件服务器

            server.login(email_user, password)
            text = msg.as_string()

            try:
                server.sendmail(email_user, email_send, text)
                print(f"[+] Email Send Successful | To: %s"%(email_send))
            except Exception as e:
                error_log = "error.log"
                with open(error_log, "a") as log:
                    log.write("Failed to Send Mail To:%s || Exception: %s"%(email_send, e))

            server.quit()

def gen_qrcode(url):
    buffer = io.BytesIO()
    embedded_qr = create(url)
    embedded_qr.png(buffer, scale=7)
    qrcode_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return qrcode_b64

if __name__ == "__main__":
    send_mail()