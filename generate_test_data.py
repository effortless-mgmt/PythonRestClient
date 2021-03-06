import sys
from user_role_creation import UserRoleCreator
from company_creator import create_demo_companies
from appointment_creator import create_appointments
from primary_roletype import PrimaryRoleType

def is_db_empty(user_role_creator):
    users = user_role_creator.get_users()
    if (len(users) != 0):
        return False
    return True

if (len(sys.argv) > 1):
    if (sys.argv[1] == "staging"):
        api_url = "https://staging.effortless.dk/api"
    elif (sys.argv[1] == "prod" or sys.argv[1] == "production"):
        api_url = "https://api.effortless.dk/api"
    elif (sys.argv[1] == "local"):
        api_url = "http://localhost:5000/api"
    elif (sys.argv[1] == "local.ssl"):
        api_url = "https://localhost:5001/api"
    else:
        api_url = "http://localhost:5000/api"
urc = UserRoleCreator(api_url)
# Make sure the database is empty
# if (not is_db_empty(urc)):
#     print("Data has already been generated. Please reset the database before running this script.")
#     sys.exit(-1)
print(f"Adding data to server: {api_url}")
    
print("\n========== Creating Roles with Privileges ==========\n")
random_mainuser = urc.generate_random_user("jd", "SecurePassword")
main_user = urc.create_user(random_mainuser)
auth = urc.login("jd", "SecurePassword")
token = auth["token"]
urc.set_token(token)
from threading import Thread

admin = urc.create_role_with_privileges("admin", ["create_user", "delete_user", "modify_user"])
substitute = urc.create_role_with_privileges("substitute", ["manage_hours", "something_else"])
client = urc.create_role_with_privileges("client", ["manage_own_company", "requests_substitutes"])
booker = urc.create_role_with_privileges("booker", ["manage_substitutes", "manage_all_companies"])

print("\n========== Creating Users ==========\n")

urc.create_random_user_with_roles("TestBooker", [booker], "SecurePassword")
urc.create_random_user_with_roles("TestUser_Admin", [admin])
urc.create_random_user_with_roles("TestUser_Client", [client])
urc.create_random_user_with_roles("TestUser_Booker", [booker])
urc.create_random_user_with_roles("TestUser_ClientBooker", [client, booker])
urc.create_random_user_with_roles("TestUser_All", [admin, substitute, client, booker])

password = "SecurePassword"
urc.create_random_user_with_roles("booker", [booker], password, PrimaryRoleType.BOOKER)
urc.create_random_user_with_roles("client", [client], password, PrimaryRoleType.CLIENT)
urc.create_random_user_with_roles("substitute", [substitute], password, PrimaryRoleType.SUBSTITUTE)

urc.create_random_user_with_roles("TestUser_Substitute01", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute02", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute03", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute04", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute05", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute06", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute07", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute08", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute09", [substitute])
urc.create_random_user_with_roles("TestUser_Substitute10", [substitute])
# t0 = Thread(target = urc.create_random_user_with_roles, args=("TestBooker", [booker], "SecurePassword"))
# t1 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Admin", [admin]))
# t2 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Client", [client]))
# t3 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Booker", [booker]))
# t4 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_ClientBooker", [client, booker]))
# t5 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_All", [admin, substitute, client, booker]))

# t6 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute01", [substitute]))
# t7 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute02", [substitute]))
# t8 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute03", [substitute]))
# t9 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute04", [substitute]))
# t10 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute05", [substitute]))
# t11 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute06", [substitute]))
# t12 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute07", [substitute]))
# t13 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute08", [substitute]))
# t14 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute09", [substitute]))
# t15 = Thread(target = urc.create_random_user_with_roles, args=("TestUser_Substitute10", [substitute]))

# threads = [t0, t1, t2, t3, t4, t5, t6, t8, t9, t10, t11, t12, t13, t14, t15]

# for thread in threads:
#     thread.start()
# for thread in threads:
#     thread.join()

print("\n========== Creating Companies ==========\n")

create_demo_companies(token, api_url)

print("\n========== Creating Agreements ==========\n")

create_appointments(token, api_url)
