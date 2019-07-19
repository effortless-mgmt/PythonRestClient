from datetime import datetime
from requests import Session, Request
import requests
from token_helper import TokenHelper
from data_generator import DataGenerator

class EffortlessApi:
    def __init__(self, base_url, verify_ssl=True):
        self.base = base_url
        self.session = Session()
        self.token = None
        self.verify_ssl = verify_ssl
    
    def login(self, username, password):
        user = {"username": username, "password": password}
        
        resp = self.session.post(f"{self.base}/auth/login", json=user, verify=self.verify_ssl)
        
        if resp.status_code == 500:
            return None

        tokenObj = resp.json()

        self.token = tokenObj["token"]

        return tokenObj
    
    def is_logged_in(self):
        if self.token == None:
            return False
        if TokenHelper.is_expired(self.token):
            self.token = None
            return False

        return True
    
    def create_user(self, user):
        url = f"{self.base}/user"

        # profile_pic = requests.get("https://randomuser.me/api/?inc=picture&nat=dk&results=1").json()["results"][0]["picture"]["large"]
        profile_pic = f"https://api.adorable.io/avatars/285/{user['userName']}.png"
        user["profilePictureUrl"] = profile_pic
        resp = self.session.post(url, json=user, verify=self.verify_ssl)

        if resp.status_code == 500:
            return None
        
        return resp.json(), resp.status_code

    def get(self, resource):
        if not self.is_logged_in():
            return None

        url = f"{self.base}/{resource}"

        authheader={"Authorization": f"Bearer {self.token}"}
        resp = self.session.get(url, headers=authheader, verify=self.verify_ssl)

        if resp.status_code < 200 or resp.status_code > 201:
            print(f"Failed GET to {url}.")
            return resp.text, resp.status_code
        return resp.json(), resp.status_code

    def post(self, resource, jsonBody=None):
        if not self.is_logged_in():
            return None
            
        url = f"{self.base}/{resource}"
        authheader={"Authorization": f"Bearer {self.token}"}

        if jsonBody == None:
            resp = self.session.post(url, headers=authheader, verify=self.verify_ssl)
        else:
            resp = self.session.post(url, json=jsonBody, headers=authheader, verify=self.verify_ssl)

        if resp.status_code < 200 or resp.status_code > 201:
            print(f"Failed POST {jsonBody} to {url}.")
            return resp.text, resp.status_code
        
        created = resp.json()

        print("OK, id:", created['id'])
        return resp.json(), resp.status_code

if __name__ == "__main__":
    demouser = DataGenerator.demo_user()
    # api = EffortlessApi("http://localhost:5000/api")
    api = EffortlessApi("https://staging.effortless.dk/api")

    auth = api.login(demouser["userName"], demouser["password"])
    if (api.is_logged_in()):
        print(f"Logged in as {auth['user']['firstName']} {auth['user']['lastName']}.")
    else:
        print(f"Could not log in. User {demouser['userName']} might not exist, or the API might be down.")
