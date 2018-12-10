import sys
import requests, json
# import multiprocessing.dummy as mp
from threading import Thread

api_url = "https://api.effortless.dk/api"

def get_users():
    return requests.get(f"{api_url}/user").json()

def delete_user(username):
    print(f"Deleting user '{username}'")
    requests.delete(f"{api_url}/user/{username}")

def users_to_delete(users):
    # if(len(users_to_delete) == 1 and users_to_delete[0]["userName"] == "jd"):
    #     return False
    # if(len(users_to_delete) == 0):
    #     return False
    # return True
    deletable_users = []
    for user in users:
        if (user["userName"] == "jd"):
            continue
        deletable_users.append(user)
    return deletable_users

def delete_users(users):
    deleted_users_count = 0
    if(len(users_to_delete(users)) == 0):
        print("No users to delete.")
        return
    
    users = users_to_delete(users)
    for user in users:
        delete_user(user["userName"])
        deleted_users_count += 1
        # Thread(target = delete_user, args = user["userName"]).start()
    print(f"Successfully deleted {deleted_users_count} users.")

if(__name__ == "__main__"):
    if (len(sys.argv) == 2):
        api_url = sys.argv[1]
    print(f"Using {api_url}")
    users = get_users()
    count = delete_users(users)
