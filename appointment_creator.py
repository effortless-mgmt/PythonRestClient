import requests, json
import random, string, time, calendar
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date

class AppointmentCreator:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def get_companies(self):
        companies = requests.get(f"{self.api_url}/company").json()

        for company in companies:
            company["departments"] = requests.get(f"{self.api_url}/company/{company['id']}/departments").json()
        
        return companies
    
    def get_users(self):
        return requests.get(f"{self.api_url}/user").json()
    def get_users_with_role(self, rolename):
        roles = requests.get(f"{self.api_url}/role?rolename={rolename}").json()
        
        if len(roles) == 0:
            return None

        role = roles[0]

        return requests.get(f"{self.api_url}/user?roleid={role['id']}").json()
    
    def create_agreement(self, agreement):
        agreement = requests.post(f"{self.api_url}/agreement", json=agreement)
        agreement = agreement.json()
        print(f"Created agreement {agreement['name']} with id {agreement['id']}")
        return agreement

    def create_workperiod(self, workperiod):
        workperiod = requests.post(f"{self.api_url}/workperiod", json=workperiod).json()
        print(f"Created workperiod {workperiod['name']} with id {workperiod['id']}")
        return workperiod

    def create_appointment(self, appointment):
        appointment = requests.post(f"{self.api_url}/appointment", json=appointment).json()
        print(f"Created appointment from {appointment['start']} to {appointment['stop']} with id {appointment['id']}")
        return appointment
    
    def add_user_to_workperiod(self, username, workperiod_id):
        resp = requests.post(f"{self.api_url}/user/{username}/workperiod/{workperiod_id}").json()
        print(f"Added user {username} to work period \"{resp['name']}\" (id: {workperiod_id})")
        return resp
    
    def random_appointment(self, user_id, workperiod_id):
        d1 = self.random_date_past()
        d2 = self.random_date_future()
        work_date = random.choice([d1, d2])

        work_from = datetime(work_date.year, work_date.month, work_date.day, 8, 0, 0)
        work_to = datetime(work_date.year, work_date.month, work_date.day, 17, 0, 0)

        time_break = random.randint(30, 61)
        
        return { "start": work_from.isoformat(), "stop": work_to.isoformat(), "break": time_break, "ownerId": user_id, "workperiodId": workperiod_id }
    
    def random_work_period(self, department_id, agreement_id):
        names = ["Storage", "Cassier", "Fork Lift", "Programmer", "Consultant", "Teaching Assistant", "Floor Manager", "Driver"]

        start_date = self.random_date_past_long()
        name = f"{random.choice(names)} - {calendar.month_name[start_date.month]}"
        
        return { "name": name, "departmentId": department_id, "agreementId": agreement_id, "start": datetime(start_date.year, start_date.month, start_date.day, 8, 0 ,0).isoformat()}

    def random_agreement(self, agreement_name):
        name = f"{''.join(random.choice(string.ascii_uppercase) for x in range(3))} {agreement_name} FWP-{random.randint(10,100)}"
        version = f"{date.today().year}-{random.randint(1,date.today().month + 1)}"
        salary = random.randint(110, 251)
        unitprice = random.randint(100,201) + salary
        nightsubsidy = random.randint(20, 100)
        weekendsubsidy = random.randint(20, 100)
        holidaysubsidy = random.randint(20, 100)
        
        return { "name" : name, "version" : version, "salary" : salary, "unitprice" : unitprice, "nightsubsidy" : nightsubsidy, "weekendsubsidy" : weekendsubsidy, "holidaysubsidy": holidaysubsidy }

    def random_date_past_long(self):
        start = (date.today() + relativedelta(months=-24)).toordinal()
        end = date.today().toordinal()

        return date.fromordinal(random.randint(start, end))

    def random_date_past(self):
        start = (date.today() + relativedelta(months=-1)).toordinal()
        end = date.today().toordinal()

        return date.fromordinal(random.randint(start, end))

    def random_date_future(self):
        start = date.today().toordinal()
        end = (date.today() + relativedelta(months=+1)).toordinal()

        return date.fromordinal(random.randint(start, end))

def create_appointments(url = "http://localhost:5000/api"):
    ac = AppointmentCreator(url)

    ag01 = ac.create_agreement(ac.random_agreement("Agreement_01"))
    ag02 = ac.create_agreement(ac.random_agreement("Agreement_02"))

    companies = ac.get_companies()
    workperiods = []

    print("\n=== Creating Workperiods ===\n")

    for company in companies:
        for department in company['departments']:
            # Choose an agreement for the department
            agreement = random.choice([ag01, ag02])
            # Create a work period
            workperiod = ac.create_workperiod(ac.random_work_period(department['id'], agreement['id']))
            # Add the new workperiod to a list
            workperiods.append(workperiod)

    print("\n=== Creating Appointments ===\n")

    # import pprint
    # pp=pprint.PrettyPrinter(indent=4)
    users = ac.get_users_with_role("substitute")
    # workperiods = requests.get(f"{url}/workperiod").json()

    for user in users:
        print(f"User: {user['userName']}")
        # Get two random work periods
        wps = random.sample(workperiods, random.randint(0,6))

        # Add user to each of the work periods
        for wp in wps:
            # Add a user to one or more work periods
            wp = ac.add_user_to_workperiod(user['userName'], wp['id'])

            appointment_threads = []

            # Add between 5 and 15 appointments for the user
            for _ in range(random.randint(0, 10)):
                ac.create_appointment(ac.random_appointment(user['id'], wp['id']))
        print()

if __name__ == "__main__":
    create_appointments()
    # test()
