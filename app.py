from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:kwakwa5!@localhost/height_collector"
db = SQLAlchemy(app)
db.init_app(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)
    
    def __init__(self,email_, height_):
        self.email_ = email_
        self.height_ = height_
    

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        email = request.form["email_name"]
        height = request.form["height_name"]
        if not db.session.query(Data).filter(Data.email_== email).count():
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            
            height_sum = db.session.query(func.sum(Data.height_)).scalar()   
            amount = db.session.query(Data).count()       
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
                
            return render_template("success.html")
        
        return render_template("index.html",
                               text="That email already exists.")
        


if __name__ == "__main__":
    app.debug = True
    with app.app_context():
        db.create_all()
    app.run()
