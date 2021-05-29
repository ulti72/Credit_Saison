from flask import Flask, render_template, url_for , request
import requests
from flaskapi import app
from flaskapi.models import User
from flaskapi import db

@app.route("/card_scheme/verify/", methods=['GET','POST'])
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
    res = 'true'
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
           
            return  {
                'success': 'false',
                'payload': {
                'bank': 'not_found',
                'type': 'not_found',
                'scheme': 'not_found' 
                }
    }

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
        'success': res,
        'payload': {
        'bank': bank,
        'type':card_type ,
        'scheme': scheme 
        }
    }

    return result 



@app.route('/card_scheme/stats', methods=['GET'])
def hits():
    start = request.args.get('start') or  1
    lm = request.args.get('limit') or 10

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
