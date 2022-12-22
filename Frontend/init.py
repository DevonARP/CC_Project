from flask import Flask, render_template, request, session, url_for, redirect, flash
import requests
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    Email = session['Email']
    return render_template('home.html', Email=Email)

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#logout page
@app.route('/logout')
def logout():
    session.pop('Email')
    return redirect('/')

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    Email = request.form['Email']
    Password = request.form['password']
#https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/get-values?email=test8&password=test
    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/get-values?email="
    url =url+ Email + "&password=" + Password
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response = json.loads(response.text)
    print(response['data']['data'])
    if(response['data']['data']==None):
        return render_template('index.html', error='Error: No account found')
    else:
        session['Email'] = Email
        return redirect(url_for('home'))


#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#RDS-post
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    fName = request.form['fName']
    lName = request.form['lName']
    Email = request.form['Email']
    Contact = request.form['Contact']
    Password = request.form['Password']
#https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/post-data?fname=JayK&lname=dude&email=abcdef@nyu.edu&contact=65826238&reward=0&promo=0&password=hiy
    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/post-data?fname="
    url =url+ fName + "&lname=" + lName + "&email=" + Email + "&contact=" + Contact + "&password=" + Password
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text)
    print(response['data'])
    if(response['data']=='Error: Email alrady in system.'):
        return render_template('index.html', error=response['data'])
    else:
        return render_template('index.html', error='Successfully created an account!')

@app.route('/location')
def location():
    Email = session['Email']
    return render_template('location.html', Email = Email)

@app.route('/specify', methods=['GET', 'POST'])
def specify():
    Email = session['Email']
    start = request.form['start']
    end = request.form['end']
    date = request.form['date']
#https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/get-values?email=test8&password=test
    url='https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/trip?start='
    url = url + start + "&end=" + end + "&date=" + date

    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    data=data['data']
    print(len(data))
    if(len(data)>0):
        print(data)
        url='https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/get-price?pick='
        url = url + start + "&drop=" + end
        payload={}
        headers = {
        'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        price=response.text
        price=json.loads(price)
        price=price['data']
        price=price['data']
        global tripprice
        tripprice = price
        print(price)
        return render_template('list.html', Email = Email, data=data, price=price)
    else:
        return render_template('home.html', Email = Email, error='Error: No trip planned.')
    
@app.route('/book', methods=['GET', 'POST'])
def book():
    Email = session['Email']
    global bookid 
    bookid = request.form['id']
#https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/get-price?pick=New York&drop=Atlanta
    url='https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/payment?email='
    url = url + Email

    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    print(data)
    if(data=='Error: No payment.'):
        return render_template('home.html', Email = Email, error='Error: No payment method.')
    else:
        url='https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/bookingid?id='
        url = url + bookid
        payload={}
        headers = {
        'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        trip=response.text
        trip=json.loads(trip)
        print(trip)
        trip=trip['data']
        print(trip)
        trip=trip['data']
        print(trip)
        return render_template('confirm.html', Email = Email, data=data,trip=trip,price=tripprice)
    
@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    Email = session['Email']
    pay = request.form['pay']
#https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/get-price?pick=New York&drop=Atlanta
    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/createbooking?email=test4&card=123&price=34&id=1"
    url='https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/createbooking?email='
    print(tripprice[0])
    url = url + Email + '&card=' + pay + '&price=' + str(tripprice[0]) + '&id=' + bookid 
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response = json.loads(response.text)
    print(response['data'])
    if(response['data']=='Error: Already registered for this trip.'):
        return render_template('home.html', Email = Email, error=response['data'])
    elif(response['data']=='Booked but please verify email.'):
        return render_template('home.html', Email = Email, error='Booked but please verify email.')
    else:
        return render_template('home.html', Email = Email, error='Successfully booked trip!')

@app.route('/upcoming')
def upcoming():
    Email = session['Email']
    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/upcoming?email="
    url = url + Email
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    print(data)
    data=data['data']
    print(data)
    data=data['data']
    print(data)
    if(len(data)>0):
        return render_template('upcoming.html', Email=Email,data=data)
    else:
        return render_template('home.html', Email=Email,error='Error: No upcoming trips planned.')

@app.route('/refund', methods=['GET', 'POST'])
def refund():
    Email = session['Email']
    bid = request.form['id']
    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/refund?email="
    url = url + Email + '&id=' + bid
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    print(data)
    if(data['data']=='Deleted but please verify email.'):
        return render_template('home.html', Email = Email, error='Deleted but please verify email.')
    else:
        return render_template('home.html', Email=Email, error='Trip is refunded.')

@app.route('/profile')
def profile():
    Email = session['Email']
    print(Email)
    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/profile?email="
    url=url+Email
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    data=data['data']
    print(data)
    return render_template('profile.html', Email = Email, data=data)

@app.route('/profileupdate', methods=['GET', 'POST'])
def profileupdate():
    Email = session['Email']
    first = request.args['first']
    last = request.args['last']
    email2 = request.args['email']
    contact = request.args['contact']
    password = request.args['password']

    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/profileupdate?email="
    #test4&first=Devon&last=Poonai&email2=test&contact=347&password=return"
    url = url + Email + '&first=' + first + '&last=' + last + '&email2=' + email2 + '&contact=' + contact + '&password=' + password
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    print(data)
    return render_template('home.html', Email = Email, error=data)

@app.route('/Past')
def Past():
    Email = session['Email']
    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/pasttrips?email="
    url=url+Email
    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    data=data['data']
    print(data)
    if(data):
        return render_template('past.html', Email = Email, data=data)
    else:
        return render_template('home.html', Email = Email, error='No past trips were found.')

@app.route('/Payments')
def Payments():
    Email = session['Email']

    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/payments?email="
    url=url+Email

    payload={}
    headers = {
    'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    data=data['data']
    print(data)
    return render_template('payments.html', Email = Email, data=data)

@app.route('/paymentupdate', methods=['GET', 'POST'])
def paymentupdate():
    Email = session['Email']
    ctype = request.args['type']
    card = request.args['Card']
    date = request.args['date']
    csv = request.args['CSV']

    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/addpayment?email="
    #test4&ctype=Credit&card=111111&date=2022-12-06&csv=123
    url=url+Email+'&ctype='+ctype+'&card='+card+'&date='+date+'&csv='+csv
    payload={}
    headers = {
      'x-api-key': 'e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    print(data)

    return render_template('home.html', Email = Email, error=data)

@app.route('/removecard', methods=['GET', 'POST'])
def removecard():
    Email = session['Email']
    card = request.form['id']

    url = "https://5s30wt52qj.execute-api.us-east-1.amazonaws.com/first_test/payments/removecard?email="
    url=url+Email+'&card='+card

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    data=response.text
    data=json.loads(data)
    data=data['data']
    print(data)
    return render_template('home.html', Email = Email, error=data)

@app.route('/store')
def store():
    Email = session['Email']
    return render_template('store.html', Email = Email)

app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
    #app.run(debug=True, ssl_context='adhoc')
    app.run(debug=True, host='0.0.0.0', port=8080, ssl_context='adhoc')