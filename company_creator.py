import requests, json
from threading import Thread
from multiprocessing.pool import ThreadPool

class CompanyCreator:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def get_companies():
        return requests.get(f"{api_url}/company").json()
    def get_departments():
        return requests.get(f"{api_url}/department").json()
    def get_agreements():
        return requests.get(f"{api_url}/agreement").json()
    def get_appointments():
        return requests.get(f"{api_url}/appointment").json()

    def create_company(self, company):
        req = requests.post(f"{self.api_url}/company", json=company)

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None
        
        company = req.json()
        print(f"Created company {company['name']} with id {company['id']}.")

        return company
    
    def create_department(self, department):
        req = requests.post(f"{self.api_url}/department", json=department)

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None
        
        department = req.json()
        print(f"Created department {department['name']} with id {department['id']}.")

        return department
    
    def create_company_with_departments(self, vat, country="dk"):
        req = requests.get(f"https://cvrapi.dk/api?vat={vat}&country={country}")

        if (req.status_code < 200 and req.status_code > 201):
            print("Dunno what happened")
            print(req.text)
            return None

        requestedCompany = req.json()

        company = {
            "vat": requestedCompany["vat"],
            "name": requestedCompany["name"],
            "pno": "0",
            "address": {
                "street": requestedCompany["address"],
                "city": requestedCompany["city"],
                "zipCode": requestedCompany["zipcode"],
                "no": -1,
                "country": "Danmark"
            }
        }

        # print(company)
        # return
        self.create_company(company)
        # create_company_thread = Thread(target = self.create_company, args=(company))
        # create_company_thread.start()

        prod_units = []

        for reqPu in requestedCompany['productionunits']:
            pu = {
                "pno": reqPu["pno"],
                "name": reqPu["name"],
                "company": {
                    "vat": vat
                },
                "address": {
                    "street": requestedCompany["address"],
                    "city": requestedCompany["city"],
                    "zipCode": requestedCompany["zipcode"],
                    "no": -1,
                    "country": "Danmark"
                }
            }

            self.create_department(pu)
            # prod_units.append(Thread(target = self.create_department, args=(pu)))

        # create_company_thread.join()

        # for pu in prod_units:
        #     pu.start()
        # for pu in prod_units:
        #     pu.join()

        print(f"Sucessfully created company {company['name']} ({vat}) with all production units.\n")
    
def create_demo_companies(url = "http://localhost:5000/api"):
    creator = CompanyCreator(url)
    creator.create_company_with_departments(35783482)
    creator.create_company_with_departments(19766241)
    creator.create_company_with_departments(32939635)
    creator.create_company_with_departments(30060946)

if __name__ == "__main__":
    create_demo_companies()
    