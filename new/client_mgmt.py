from data_generator import DataGenerator

class ClientManager:
    def __init__(self, api):
        self.api = api
    
    def create_company(self, company):
        print(f"- Creating company {company['name']}... ", end="")
        created, code = self.api.post("company", company)
        return created, code
    
    def create_department(self, production_unit):
        print(f"   - {production_unit['name']}... ", end="")
        created, code = self.api.post("department", production_unit)
        return created, code
    
    def create_company_with_departments(self, vat, country="dk"):
        print("VAT", vat)
        company, produnits = DataGenerator.get_company(vat, country)

        created_company, code = self.create_company(company)

        if code != 200 and code != 201:
            return None, code
        
        for pu in produnits:
            dep, code = self.create_department(pu)

            if code != 200 and code != 201:
                print("Failed to create dapartment. Skipping...")
                continue
            

