import sys
from user_role_creation import UserRoleCreator
from company_creator import create_demo_companies

def is_db_empty(user_role_creator):
    users = user_role_creator.get_users()
    if (len(users) != 0):
        return False
    return True

if (len(sys.argv) > 1):
    if (sys.argv[1] == "staging"):
        api_url = "https://staging.effortless.dk/api"
    elif (sys.argv[1] == "prod" or sys.argv[1] == "production"):
        api_url == "https://api.effortless.dk/api"
    elif (sys.argv[1] == "local"):
        api_url = "http://localhost:5000/api"
    elif (sys.argv[1] == "local.ssl"):
        api_url = "https://localhost:5001/api"
    else:
        api_url = "http://localhost:5000/api"
urc = UserRoleCreator(api_url)

# Make sure the database is empty
if (not is_db_empty(urc)):
    print("Data has already been generated. Please reset the database before running this script.")
    sys.exit(-1)
print(f"Adding data to server: {api_url}")
    
from threading import Thread
print("\n========== Creating Roles with Privileges ==========\n")

admin = urc.create_role_with_privileges("admin", ["create_user", "delete_user", "modify_user"])
substitute = urc.create_role_with_privileges("substitute", ["manage_hours", "something_else"])
client = urc.create_role_with_privileges("client", ["manage_own_company", "requests_substitutes"])
booker = urc.create_role_with_privileges("booker", ["manage_substitutes", "manage_all_companies"])

print("\n========== Creating Users ==========\n")

t1 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Admin", [admin]))
t2 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute", [substitute]))
t3 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Client", [client]))
t4 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Booker", [booker]))
t5 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_ClientBooker", [client, booker]))
t6 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_All", [admin, substitute, client, booker]))

threads = [t1, t2, t3, t4, t5, t6]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

print("\n========== Creating Companies ==========\n")

create_demo_companies(api_url)
