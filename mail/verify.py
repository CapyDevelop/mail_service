import os

from jinja2 import Environment, FileSystemLoader
from email.header import Header
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv

load_dotenv()
print(os.path.abspath("./mail/templates"))
print(os.getcwd())
env = Environment(loader=FileSystemLoader(os.path.abspath("./mail/templates")))


def send_verify_message(nickname, code):
    content = env.get_template("verify_code.html").render({"nickname": nickname.split("@")[0], "code": code})
    print(content)
    # content = render_template("verify_code.html", nickname=nickname, code=12345)

    msg = MIMEText(content, "html", 'utf-8')
    msg['Subject'] = Header("Твой код подтверждения", 'utf-8')

    # msg['From'] = 'popov2895@mail.ru'
    msg['From'] = 'verify@capybaras21.space'
    # msg['To'] = f"{nickname}@student.21-school.ru"
    msg['To'] = f"{nickname}"
    # msg['To'] = f"timkonovalov9858@gmail.com"
    print(os.getenv("VERIFY_PASSWORD"), f"{nickname}")
    password = os.getenv("VERIFY_PASSWORD")
    # password = "gwinxxr9ecT8hkA7ckEw"

    # s = smtplib.SMTP('smtp.mail.ru', 465)
    # s = smtplib.SMTP('mail.hosting.reg.ru', 587)
    s = smtplib.SMTP('smtp.eu.mailgun.org', 587)
    print("smtp")
    s.starttls()
    print("starttls")
    s.login(msg['From'], password)
    print("login success")
    resp = s.sendmail(msg['From'], [msg['To']], msg.as_string())
    print("alya send", resp)
    s.quit()
    print("quit")
