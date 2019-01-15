import sys
import random
import requests, json
from delete_test_users import api_url

def random_users(count):
    url = f"https://randomuser.me/api/?inc=name,email,login,phone&nat=dk,uk,us&results={count}"

    reqUsers = requests.get(url).json()["results"]
    users = []

    for reqUser in reqUsers:
        users.append({
            "firstName": reqUser["name"]["first"],
            "lastName": reqUser["name"]["last"],
            "email": reqUser["email"],
            "phone": reqUser["phone"],
            "userName": reqUser["login"]["username"],
            "password": reqUser["login"]["password"]
            "primaryRoleType": random.randint(0, 2)
        })
    return users

def create_user(user):
    print(f"Creating user '{user['userName']}'")
    req = requests.post(f"{api_url}/user", json=user)

    if (req.status_code < 200 and req.status_code > 201):
        print("Dunno what happened")
        print(req.text)
        return None
    
    return req.json()

users_to_create = 10

if(len(sys.argv) > 1):
    try:
        users_to_create = int(sys.argv[1])
    except:
        print("Argument must be a number")
        sys.exit(-1)
if (len(sys.argv) == 3):
    api_url = sys.argv[2]
print(f"Using {api_url}")

users = random_users(users_to_create)

userNames = []
print("Creating users:")
for user in users:
    created_user = create_user(user)
    userNames.append(created_user["userName"])
print()
print(f"Created {users_to_create} users:")

print(userNames)
