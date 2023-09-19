import requests
import hashlib
import sys

#create function that passes the query characters to check the password
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    #create an error message if it doesn't work
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

#check what kind of data we're receiving
def get_password_leaks_count(hashes, hash_to_check):
    #return a list of the lines in the string, breaking at line boundaries
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

#check password if it exists in API response
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

#print results of all the calculations
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should change your password')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'done!'

#run function that accepts any number of arguments we pass 
main(sys.argv[1:])
