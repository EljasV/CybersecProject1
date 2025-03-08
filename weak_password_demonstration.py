import sqlite3
from random import choice

import bs4 as bs
import requests

URL = "http://localhost:8000"
unsafe_passwords = ["password", "1234", "a", "123456", "qwerty"]
safe_password = "- VEryyyy saAfe P455Swooooord ynldttj842883 1"


def main():
    remove_existing_user()
    user_makes_new_account()
    hacker_bruteforces()


def hacker_bruteforces():
    print("Hacker is trying to bruteforce password")
    found_unsafe_password = False
    password = ""
    for pw in unsafe_passwords:
        s = requests.session()
        response = s.get(URL + "/login")
        token = extract_token(response)
        response = s.post(URL + "/login/",
                          data={"csrfmiddlewaretoken": token, "password": pw, "username": "regular_user"})

        soup = bs.BeautifulSoup(response.text, "html.parser")
        # Check if we are not in login form
        if not soup.find_all("input", {"name": "username"}):
            found_unsafe_password = True
            password = pw
            break
    if found_unsafe_password:
        print("Hacker found unsafe password: " + password)
    else:
        print("Hacker did not find unsafe password")


def user_makes_new_account():
    # Simulate an unaware user creating an account with an unsafe password.
    s = requests.session()
    response = s.get(URL + "/new_account")
    token = extract_token(response)
    pw = choice(unsafe_passwords)
    response = s.post(URL + "/new_account_submit",
                      data={"csrfmiddlewaretoken": token, "password1": pw, "password2": pw, "username": "regular_user"})
    soup = bs.BeautifulSoup(response.text, "html.parser")
    # Check if we are still in login form
    if soup.find_all("form", {"action": "/new_account_submit"}):
        print("Tried to make an account with an unsafe password, but failed.")
        response = s.post(URL + "/new_account_submit",
                          data={"csrfmiddlewaretoken": token, "password1": safe_password, "password2": safe_password,
                                "username": "regular_user"})
        print("Made an account with a safe password")
    else:
        print("Made an account with an unsafe password: " + pw)


def remove_existing_user():
    print("Making sure user does not already exist in database")
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    sql = 'DELETE FROM auth_user WHERE username="regular_user"'
    cursor.execute(sql)
    conn.commit()


# Taken from Securing Software, part 4 exercise 19
def extract_token(response):
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    for i in soup.form.find_all('input'):
        if i.get('name') == 'csrfmiddlewaretoken':
            return i.get('value')
    return None


if __name__ == "__main__":
    main()
