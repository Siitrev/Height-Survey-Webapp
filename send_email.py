from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

def  send_email(email,height,height_sum,amount):
    ctx = ssl.create_default_context()
    password = "emcdjmsppoyvwjnq"    
    sender = "dcollector673@gmail.com"    
    receiver = email  

    message = MIMEMultipart("alternative")
    message["Subject"] = f'Hello {email}'
    message["From"] = sender
    message["To"] = receiver

    html = f"""\
    <html>
    <body>
        <p>
            <i>Hello {email}</i>
        </p>
        <p>
            That's your height: <strong>{height}</strong>
            Here's the average height of <strong>{amount}</strong> people who completed the survey: <strong>{round(height_sum/amount,2)}</strong>
        </p>
    </body>
    </html>
    """

    plain = f"""\
    Hello {email}.
    That's your height: {height}
    Here's the average height of {amount} people who completed the survey: {round(height_sum/amount,2)}
    """

    message.attach(MIMEText(plain, "plain"))
    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
                