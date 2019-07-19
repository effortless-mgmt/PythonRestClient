import sys, random
from api import EffortlessApi
from data_generator import DataGenerator
from demodata import demousers, demoroles
from primary_roletype import PrimaryRoleType

from user_mgmt import UserManager
from role_mgmt import RoleManager
from client_mgmt import ClientManager
from job_mgmt import JobManager

# baseurl = "http://localhost:5000/api"
baseurl = "https://staging.effortless.dk/api"
# baseurl = "https://api.effortless.dk/api"
api = EffortlessApi(baseurl, verify_ssl = True)

#####################
# Consistent Logins #
#####################

demouser = DataGenerator.demo_user()
auth = api.login(demouser["userName"], demouser["password"])

# Create demo user
if auth != None:
    print("Users have already been created. Please reset the database.")
    print(auth)
    sys.exit(-1)
else:
    user, code = api.create_user(demouser)
    if code == 201:
        print("User created:", user)
    elif code == 200:
        print("User already exist:", user)
        sys.exit(-1)
    else:
        print("Some other error occured:", code)
        sys.exit(-1)

# Create users with specific roles
auth = api.login(demouser["userName"], demouser["password"])
api.create_user(DataGenerator.q_user())

###############################
# Create Roles and Demo Users #
###############################

rolemgmt = RoleManager(api)
usermgmt = UserManager(api, rolemgmt)
# booker, client, substitute = demousers()
demousers = demousers()
demoroles = demoroles()

if len(demousers) != len(demoroles):
    print("This is a hacky application, meaning demousers and demoroles MUST be of equal length......")

# Create the demousers
for i in range(len(demousers)):
    print(i + 1, "/", len(demousers))
    usermgmt.create_user_with_roles(demousers[i], [demoroles[i]])

# usermgmt.create_random_users_with_roles(10, demoroles)
usermgmt.create_random_substitute_with_name("substitute01")
usermgmt.create_random_substitute_with_name("substitute02")
usermgmt.create_random_substitute_with_name("substitute03")
usermgmt.create_random_substitute_with_name("substitute04")
usermgmt.create_random_substitute_with_name("substitute05")
usermgmt.create_random_substitute_with_name("substitute06")
usermgmt.create_random_substitute_with_name("substitute07")
usermgmt.create_random_substitute_with_name("substitute08")
usermgmt.create_random_substitute_with_name("substitute09")
usermgmt.create_random_substitute_with_name("substitute10")
####################################
# Create Companies and Departments #
####################################

clientmgmt = ClientManager(api)
clientmgmt.create_company_with_departments(18922800) # Jacob Nordfalk
clientmgmt.create_company_with_departments(35783482) # Wiberg Tech
clientmgmt.create_company_with_departments(32939635) # IT Minds
clientmgmt.create_company_with_departments(17571559) # De Ingeiorstuderendes Lokalradio
clientmgmt.create_company_with_departments(19766241) # Soren Thestrup
# clientmgmt.create_company_with_departments(30060946) # DTU

##############
# Setup Jobs #
##############

jobmgmt = JobManager(api)

ag1, _ = jobmgmt.create_random_agreement("AG01")
ag2, _ = jobmgmt.create_random_agreement("AG02")

companies, _ = api.get("company")
workperiods = []

for company in companies:
    # departments, _ = api.get(f"company/{company['id']}/departments")
    departments, _ = api.get(f"company/{company['id']}/departments")
    company["departments"] = departments
    for department in company['departments']:
        agreement = random.choice([ag1, ag2])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiods.append(workperiod)
    
substitutes, _ = usermgmt.get_users_with_role(PrimaryRoleType.SUBSTITUTE)

jobmgmt.create_random_appointments(25, substitutes, workperiods)
jobmgmt.create_random_available_appointments(10)
