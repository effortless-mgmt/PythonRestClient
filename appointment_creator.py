import requests, json
import random, string, time, calendar
import dateutil.relativedelta
from datetime import datetime

class AppointmentCreator:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def get_companies(self):
        companies = requests.get(f"{self.api_url}/company").json()

        for company in companies:
            company["departments"] = requests.get(f"{self.api_url}/company/{company['id']}/departments").json()
        
        return companies
    
    def create_agreement(self, agreement):
        return requests.post(f"{self.api_url}/agreement").json()
    
    def random_work_period(self, department_id, agreement_id):
        names = ["Storage", "Cassier", "Fork Lift", "Programmer", "Consultant", "Teaching Assistant", "Floor Manager", "Driver"]


    def random_agreement(self, agreement_name):
        name = f"{''.join(random.choice(string.ascii_uppercase) for x in range(3))} {agreement_name} FWP-{random.randint(10,100)}"
        version = f"{datetime.now().year}-{random.randint(1,13)}"
        salary = random.randint(110, 251)
        unitprice = random.randint(100,201) + salary
        nightsubsidy = random.randint(20, 100)
        weekendsubsidy = random.randint(20, 100)
        holidaysubsidy = random.randint(20, 100)
        
        return { "name" : name, "version" : version, "salary" : salary, "unitprice" : unitprice, "nightsubsidy" : nightsubsidy, "weekendsubsidy" : weekendsubsidy, "holidaysubsidy": holidaysubsidy }
    
    def random_date_previous(self, to_date, from_date):
        year = random.randint(to_date.year, from_date.year)
        month = random.randint(from_date.month, to_date.month)
        monthrange = calendar.monthrange(year, month)
        day = random.randint(monthrange[0], monthrange[1])

        return datetime(year, month, day)
    
    def random_date_future(self, to_date, from_date):
        year = random.randint(to_date.year, from_date.year)
        month = random.randint(from_date.month, to_date.month)
        monthrange = calendar.monthrange(year, month)
        day = random.randint(monthrange[0], monthrange[1])

        return datetime(year, month, day)
    
    def random_previous_date(self):
        today = datetime.now()
        # Three months back at most
        previous = today + dateutil.relativedelta.relativedelta(months=-3)

        year = random.randint(previous.year, today.year)
        month = random.randint(previous.month, today.month)
        monthrange = calendar.monthrange(year, month)
        day = random.randint(monthrange[0], monthrange[1])

        return datetime(year, month, day)
    
    def random_future_date(self):
        today = datetime.now()
        # Three months ahead at most
        future = today + dateutil.relativedelta.relativedelta(months=+3)

        year = random.randint(today.year, future.year)
        month = random.randint(today.month, future.month)
        monthrange = calendar.monthrange(year, month)
        day = random.randint(monthrange[0], monthrange[1])

        return datetime(year, month, day)

def create_appointments(url = "http://localhost:5000/api"):
    ac = AppointmentCreator(url)
    # ac.get_companies()
    ag01 = ac.random_agreement("Agreement_01")
    ag02 = ac.random_agreement("Agreement_02")

    for company in ac.get_companies():
        print(company['name'])
        for department in company['departments']:
            agreement = random.choice([ag01, ag02])
            print("-", department['name'], "--", agreement['name'])
    print("\nprevious", ac.random_previous_date())
    print("future", ac.random_future_date())
    print("=====\n","today",datetime.now())

if __name__ == "__main__":
    create_appointments()
