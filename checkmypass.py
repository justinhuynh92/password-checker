import requests
import hashlib

#create function that passes the query characters to check the password
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    #create an error message if it doesn't work
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

#check password if it exists in API response
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return sha1password

pwned_api_check('123')
