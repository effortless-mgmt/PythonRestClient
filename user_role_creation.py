import sys
import requests, json
import random
from primary_roletype import PrimaryRoleType

class UserRoleCreator():
    def __init__(self, api_url, token = None):
        self.api_url = api_url
        self.set_token(token)
    
    def set_token(self, token):
        self.headers = {'Authorization': f'Bearer {token}'}

    def login(self, username, password):
        req = requests.post(f"{self.api_url}/auth/login", json={"username":username, "password":password})
        
        if (req.status_code != 200):
            print("Failed to sign in:")
            print(req.text)
            sys.exit(-1)
            
        print(f"Successfully signed in as {req.json()}")
        return req.json()

    def create_user(self, user):
        # return req.text
        req = requests.post(f"{self.api_url}/user", json=user)

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None
        
        user = req.json()
        print(f"Created user {user['userName']} with id {user['id']}.")

        return user
    
    def get_users(self):
        return requests.get(f"{self.api_url}/user").json()
    def get_user(self, username):
        return requests.get(f"{self.api_url}/user/{username}", headers=self.headers).json()

    def create_role(self, role):
        req = requests.post(f"{self.api_url}/role", json=role, headers=self.headers)

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None

        role = req.json()
        print(f"Created role {role['name']} with id {role['id']}.")

        return role
    def get_roles():
        return requests.get(f"{self.api_url}/role", headers=self.headers).json()
    def get_role(self, role_id):
        return requests.get(f"{self.api_url}/role/{role_id}", headers=self.headers).json()

    def create_privilege(self, privilege):
        req = requests.post(f"{self.api_url}/privilege", json=privilege, headers=self.headers)

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None
        
        privilege = req.json()
        print(f"Created privilege {privilege['name']} with id {privilege['id']}.")

        return privilege

    def assign_priv_to_role(self, role_id, privilege_id):
        req = requests.post(f"{self.api_url}/role/{role_id}/privilege/{privilege_id}", headers=self.headers)

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None
        
        rp = req.json()
        print(f"Assigned privilege {rp['privilege']['name']} to role {rp['role']['name']}")

        return rp

    def assign_role_to_user(self, user_id, role_id):
        req = requests.post(f"{self.api_url}/user/{user_id}/role/{role_id}", headers=self.headers)

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None

        ur = req.json()
        role = requests.get(f"{self.api_url}/role/{role_id}", headers=self.headers).json()
        print(f"Assigned role {role['name']} to role {ur['userName']}")
        
        return req.json()
    
    def create_role_with_privileges(self, role_name, privilege_names):
        role = self.create_role({ 'name': role_name })

        for privilege_name in privilege_names:
            priv = self.create_privilege({ 'name': privilege_name })
            self.assign_priv_to_role(role['id'], priv['id'])
        
        return self.get_role(role['id'])
    
    def generate_random_user(self, username, password = None, primary_role = PrimaryRoleType(random.randint(0, 2))):
        url = f"https://randomuser.me/api/?inc=name,email,login,phone&nat=dk&results=1"

        req = requests.get(url)
        try:
            reqUser = req.json()["results"][0]
        except:
            print("\n========== FAILURE =========")
            print("Failed something for user:", username)
            print(req.text)
            print("========== FAILURE =========\n")

        user = {
            "firstName": reqUser["name"]["first"],
            "lastName": reqUser["name"]["last"],
            "email": reqUser["email"],
            "phone": reqUser["phone"],
            "userName": username,
            "password": reqUser["login"]["password"],
            "primaryRoleType": primary_role.value
        }

        if password is not None:
            user['password'] = password

        return user
    
    def create_random_user_with_roles(self, username, roles, password = None, primary_role = PrimaryRoleType(random.randint(0, 2))):
        random_user = self.generate_random_user(username, password, primary_role)
        actual_user = self.create_user(random_user)

        for role in roles:
            user = self.assign_role_to_user(actual_user['userName'], role['id'])

        return user

    def list_users_with_privs(self):
        users = self.get_users()

        from threading import Thread
        threads = []

        for user in users:
            self.list_user_with_privs(user['userName'])
        for thread in threads:
            thread.start()
                
    def list_user_with_privs(self, username):
        user = self.get_user(username)
        print(f"- User {user['userName']} now has privileges: {user['privileges']}")
