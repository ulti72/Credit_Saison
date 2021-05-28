from flask import Flask, render_template , redirect , url_for , request
import requests
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(50))
    card_type = db.Column(db.String(50))
    card_number = db.Column(db.String(50))
    scheme = db.Column(db.String(50))
    hit_count = db.Column(db.Integer)

@app.route('/card_scheme/verify/', methods=['GET','POST'])
def verify():
    card_number= ''
    result = 'true'
    if request.method == 'POST':
        card_number = request.form.get('card_number')
        user = User.query.filter_by(card_number=card_number).first()

        if user: 
            print('Getting data from database')
            user.hit_count = user.hit_count + 1
            db.session.commit()
            print(user.hit_count)
            bank = user.bank_name
            scheme = user.scheme 
            card_type = user.card_type
        else:
            print('Getting data from API')
            try:
                response = requests.get('https://lookup.binlist.net/'+card_number)
                response.raise_for_status()
                json_data =  response.json()
            except requests.exceptions.HTTPError as errh:
                result = 'false'

            try:
                bank = json_data['bank']['name']
            except: 
                bank = 'not found'
            try:
                card_type = json_data['type']
            except:
                card_type = 'not found'
            try:
                scheme = json_data['scheme']
            except:
                scheme = 'not found'

            if bank != 'not found' and card_type != 'not found' and scheme != 'not found' :
                user = User(card_number = card_number, bank_name=bank, card_type=card_type, scheme =scheme, hit_count=0)
                db.session.add(user)
                db.session.commit()

        result = {
            'success': result,
            'payload': {
            'bank': bank,
            'type':card_type ,
            'scheme': scheme 
            }
        }
        return render_template('index.html', bank = result['payload']['bank'], card_type=result['payload']['type'],scheme=result['payload']['scheme'])
    else:
        return render_template('index.html', bank = '', card_type='',scheme='')


@app.route('/card_scheme/verify/<card_number>', methods=['GET'])
def card_detail(card_number):
    result = 'true'
    user = User.query.filter_by(card_number=card_number).first()
    if user: 
        print('Getting data from database')
        user.hit_count = user.hit_count + 1
        db.session.commit()
        print(user.hit_count)
        bank = user.bank_name
        scheme = user.scheme 
        card_type = user.card_type
    else :
        print('Getting from API')
        try:
            response = requests.get('https://lookup.binlist.net/'+card_number)
            response.raise_for_status()
            json_data =  response.json()
        except requests.exceptions.HTTPError as errh:
            result = 'false'

        try:
            bank = json_data['bank']['name']
        except: 
            bank = 'not found'
        try:
            card_type = json_data['type']
        except:
            card_type = 'not found'
        try:
            scheme = json_data['scheme']
        except:
            scheme = 'not found'

        if bank != 'not found' and card_type != 'not found' and scheme != 'not found' :
            user = User(card_number = card_number, bank_name=bank, card_type=card_type, scheme =scheme, hit_count=0)
            db.session.add(user)
            db.session.commit()

    result = {
        'success': result,
        'payload': {
        'bank': bank,
        'type':card_type ,
        'scheme': scheme 
        }
    }
    return result 


@app.route('/card_scheme/stats', methods=['GET'])
def hits():
    start = request.args.get('start')
    lm = request.args.get('limit')

    users_data = User.query.order_by(User.hit_count.desc()).limit(lm).all()
    payload = {} 
    for users in users_data:
        payload[users.card_number] = users.hit_count
        
    result = {
        'success': 'true',
        'start' : start ,
        'limit' : lm, 
        'size': len(payload) , 
        'payload': payload
       
    }
    return result 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081,debug=True)

