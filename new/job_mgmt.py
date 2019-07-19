import random, calendar, string, time
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import timedelta
from datetime import date

from demodata import work_period_types
from primary_roletype import PrimaryRoleType

class JobManager:
    def __init__(self, api):
        self.api = api
    
    def create_agreement(self, agreement):
        print(f"- Creating agreement {agreement['name']}...", end="")
        created, code = self.api.post("agreement", agreement)
        return created, code
    
    def create_workperiod(self, workperiod):
        print(f"- Creating work period {workperiod['name']}...", end="")
        created, code = self.api.post("workperiod", workperiod)
        return created, code
    
    def create_appointment(self, appointment):
        print(f"- Creating appointment ({appointment['start']}-{appointment['stop']})...", end="")
        created, code = self.api.post("appointment", appointment)
        return created, code
    
    def add_user_to_workperiod(self, username, workperiod_id):
        print(f"- Adding user {username} to workperiod {workperiod_id}")
        created, code = self.api.post(f"user/{username}/workperiod/{workperiod_id}")
        return created, code
    
    def create_random_agreement(self, agreement_name):
        name = f"{''.join(random.choice(string.ascii_uppercase) for x in range(3))} {agreement_name} FWP-{random.randint(10,100)}"
        version = f"{date.today().year}-{random.randint(1, date.today().month + 1)}"
        salary = random.randint(110, 251)
        unitprice = random.randint(100,201) + salary
        nightsubsidy = random.randint(20, 100)
        weekendsubsidy = random.randint(20, 100)
        holidaysubsidy = random.randint(20, 100)
        
        agreement = {
            "name" : name,
            "version" : version,
            "salary" : salary,
            "unitprice" : unitprice,
            "nightsubsidy" : nightsubsidy,
            "weekendsubsidy" : weekendsubsidy,
            "holidaysubsidy": holidaysubsidy
        }

        print(f"- Creating Agreement {name}...", end="")
        created, code = self.api.post("agreement", agreement)
        return created, code
    
    def create_random_workperiod(self, department_id, agreement_id):
        wtype = random.choice(work_period_types)
        start_date = self.random_date_past_long()
        name = f"{wtype} - {calendar.month_name[start_date.month]}"

        workperiod = {
            "name": name,
            "departmentId": department_id,
            "agreementId": agreement_id,
            "start": datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0).isoformat()
        }

        print(f"- Creating workperiod {name}...", end="")    
        created, code = self.api.post("workperiod", workperiod)
        return created, code
    
    def create_random_appointment(self, workperiod_id, user_id = None):
        d1 = self.random_date_past()
        d2 = self.random_date_future()
        work_date = random.choice([d1, d2])

        wfrom_hour = random.randint(0,23)
        wfrom_minute = random.choice([0, 15, 30, 45])
        wfrom_second = 0
        work_from = datetime(work_date.year, work_date.month, work_date.day, wfrom_hour, wfrom_minute, wfrom_second)
        
        wto_hour = (wfrom_hour + random.randint(5, 14)) % 24
        wto_minute = random.choice([0, 15, 30, 45])
        wto_second = 0
        work_to = datetime(work_date.year, work_date.month, work_date.day, wto_hour, wto_minute, wto_second)

        if (work_to < work_from):
            work_to += timedelta(days=1)
        
        time_break = random.randint(30, 61)

        appointment = {
            "start": work_from.isoformat(),
            "stop": work_to.isoformat(),
            "break": time_break,
            "ownerId": user_id,
            "workperiodId": workperiod_id
        }

        created, code = self.create_appointment(appointment)
        return created, code
    
    def create_random_appointments(self, count, users = None, workperiods = None):
        if users == None or users == []:
            users, _ = self.api.get(f"user?primaryRole={PrimaryRoleType.SUBSTITUTE.value}")
        if workperiods == None or workperiods == []:
            workperiods, _ == self.api.get(f"workperiods")
            workperiods = random.sample(workperiods, random.randint(0, len(workperiods)))
        
        for user in users:
            print(f"- Creating appointments for user {user['userName']}")
            for workperiod in workperiods:
                print(f"   - Using workperiod {workperiod['name']}")
                for _ in range(count):
                    print("      ", end="")
                    self.create_random_appointment(workperiod['id'], user['id'])
    
    def create_random_available_appointments(self, count):
        workperiods = self.api.get(f"workperiod")
        wp = random.choice(workperiods)
        for _ in range(count):
            self.create_random_appointment(wp["id"], None)
    
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
