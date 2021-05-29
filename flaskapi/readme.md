# Flask API
Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

**T**his api is created to get data from a 3rd party API, to fetch credit/debit card details.
##### API : https://binlist.net/
 Built on [Flask](https://flask.palletsprojects.com/en/1.1.x/) and uses sqlLite database.

---
## Requirements

You need  [Python 3+](https://www.python.org/downloads/).


## Getting Started

Download from Github:

```bash
$ git clone https://github.com/ulti72/Credit_Saison.git
```


Install dependencies:

``` bash
$  pipenv install
```
Start virtual environment:
``` bash
$  pipenv shell
```
### Run app

``` bash
$ python run.py
```

Point your browser to http://127.0.0.1:5000/card_scheme/verify/ to serach card details.


### API Endpoints

###### Get card details:
* Endpoint: http://127.0.0.1:5000/card_scheme/verify/<card_number>
* parameter: card number
* response: JSON 
```
{
    "success": true
    "payload" : {
    "scheme": "visa",
    "type" : "debit",
    "bank" : "UBS"
    }
}
```
###### Get number of hits:
* Endpoint: 'http://127.0.0.1:5000/card_scheme/stats?start=<start>&limit=<limit>'
* parameters:  start and limit
* Response: JSON
```
{
    "success": true
    "start": 1,
    "limit": 3,
    "size": 133,
    "payload": {
    "545423": 5,
    "679234": 4,
    "329802": 1
    }
}
```


