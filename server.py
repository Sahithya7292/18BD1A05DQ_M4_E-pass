from flask import Flask, render_template, request,redirect,url_for
import requests
import requests_cache
from twilio.rest import Client

account_id='ACef8cbedec9bbc5e5e3d9fd678be7878c'
auth_token='bd4693bd3d267d9435dbe51641a6c4e7'

client=Client(account_id,auth_token)
app=Flask(__name__)

@app.route('/')
def Registration_form():
    return render_template('Register.html')

@app.route('/login',methods=['POST'])
def login_registration_dtls():
    if request.method=='POST':
        first_name=request.form['fname']
        last_name=request.form['lname']
        email_id=request.form['email']
        source_st=request.form['source_state']
        source_dt=request.form['source_d']
        destination_st=request.form['dest_state']
        destination_dt=request.form['destination_d']
        phoneNumber=request.form['phoneNumber']
        id_proof=request.form['idcard']
        date=request.form['dat']
        full_name=first_name+"."+last_name
        r=requests.get('https://api.covid19india.org/v5/data.json')
        json_data=r.json();
        cnt=json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
        pop=json_data[destination_st]['districts'][destination_dt]['meta']['population']
        travel_pass=((cnt/pop)*100)
        if travel_pass < 30 :
            status='CONFIRMED'
            client.messages.create(to="+91"+str(phoneNumber),from_="+19104066903",body="Dear "+
                  full_name+" "+"Your Travel From "+" "+source_dt+" "+"To "+destination_dt+
                  " Has "+status+"On "+date+".Thank You!")
            return render_template('user.html', fn=full_name,email=email_id,id=id_proof,sst=source_st,
                   ssd=source_dt,dst=destination_st,dsd=destination_dt,phn=phoneNumber,dt=date,status=status)
        else:
            status="Not Confirmed"
            client.messages.create(to="+91"+str(phoneNumber),from_="+19104066903",body="Dear "+
                  full_name+" "+"Your Travel From "+" "+source_dt+" "+"To "+destination_dt+
                  " Has "+status+"On "+date+".Thank You! Apply Later")
            return render_template('user.html', fn=full_name,email=email_id,id=id_proof,sst=source_st,
                   ssd=source_dt,dst=destination_st,dsd=destination_dt,phn=phoneNumber,dt=date,status=status)
    else:
        redirect(url_for('/'))

if __name__=="__main__":
    app.run()
#runs on   http://127.0.0.1:5000/ [default]