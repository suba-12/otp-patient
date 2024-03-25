from flask import Flask, request, render_template, redirect, session
from twilio.rest import Client
from pymongo import MongoClient
import random
import string

app = Flask(__name__)
app.secret_key = "harishbot"

mongo_uri = "mongodb+srv://harishbhalaa:harish@backend.w8koxqb.mongodb.net/"
client = MongoClient(mongo_uri)
db = client.test
otp_collection = db.otps
patient_collection = db.tech_patient_datas

account_sid = 'AC1ae2f5bf0feae2b6330a18caaf1d4cb6'          #ACaf40853e8648498d022e7bff90a21fe9
auth_token = 'fec7a323768bc6824250b828baa803d7'             #6cd8165bdbd6a249e56678292ae37a67
client = Client(account_sid, auth_token)  
twilio_number = '+14342160730'                              #+15169904081


def send_otp(phone_number):
    otp = ''.join(random.choices(string.digits, k=4))
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=twilio_number,
        to=phone_number
    )
    return otp


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/verify', methods=['POST'])
def verify():
    phone_number = request.form['phone_number']
    session['phone_number'] = phone_number
    otp = send_otp(phone_number)
    session['otp'] = otp
    return render_template('verify.html')


@app.route('/check_otp', methods=['POST'])
def check_otp():
    user_otp = request.form['otp']
    if user_otp == session['otp']:
        patient_data = patient_collection.find_one({'phone_number': session['phone_number']})
        if patient_data:
            return render_template('indexx.html', data=patient_data)
        else:
            return render_template('no_data.html')
    else:
        return "Invalid OTP"


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
