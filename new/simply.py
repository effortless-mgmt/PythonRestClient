import sys, random
from api import EffortlessApi
from data_generator import DataGenerator
from demodata import demousers, demoroles
from primary_roletype import PrimaryRoleType

from user_mgmt import UserManager
from role_mgmt import RoleManager
from client_mgmt import ClientManager
from job_mgmt import JobManager

baseurl = "https://localhost:5001/api"
api = EffortlessApi(baseurl, verify_ssl = False)

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

auth = api.login(demouser["userName"], demouser["password"])
api.create_user(DataGenerator.q_user())
rolemgmt = RoleManager(api)
usermgmt = UserManager(api, rolemgmt)
demoroles = demoroles()
clientmgmt = ClientManager(api)
clientmgmt.create_company_with_departments(32939635)
jobmgmt = JobManager(api)

ag1, _ = jobmgmt.create_random_agreement("AG")

companies, _ = api.get("company")
workperiods = []

for company in companies:
    # departments, _ = api.get(f"company/{company['id']}/departments")
    departments, _ = api.get(f"company/{company['id']}/departments")
    company["departments"] = departments
    for department in company['departments']:
        agreement = random.choice([ag1])
        workperiod, _ = jobmgmt.create_random_workperiod(department['id'], agreement['id'])
        workperiods.append(workperiod)
    
substitutes, _ = usermgmt.get_users_with_role(PrimaryRoleType.SUBSTITUTE)

jobmgmt.create_random_appointments(2, substitutes, workperiods)