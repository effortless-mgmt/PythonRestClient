from api import EffortlessApi
from data_generator import DataGenerator
from role_mgmt import RoleManager
import random
class UserManager:
    def __init__(self, api, rolemgmt = None):
        self.api = api
        if rolemgmt == None:
            self.rolemgmt = RoleManager(api)
        else:
            self.rolemgmt = rolemgmt
    
    def create_user(self, user):
        print(f"- Creating user {user['userName']}... ", end="")
        
        created, code = self.api.create_user(user)

        if code == 201 or code == 200:
            print("OK")
        else:
            print(f"ERROR: status_code: {code}")
        return created, code
    
    def create_user_with_roles(self, user, roles):
        created_user, code = self.create_user(user)

        if code == 200:
            print("   User already exists")
        
        for role in roles:
            created_role, role_code = self.rolemgmt.create_role(role)
            if role_code != 200 and role_code != 201:
                print("ERROR: Failed to create role.")
                continue
            self.rolemgmt.assign_role_to_user(created_role['id'], created_user['userName'])

    def create_random_users_with_roles(self, user_count, roles):
        print(f"Generating {user_count} random users.")
        random_users = DataGenerator.random_users(user_count)

        c = 0
        for user in random_users:
            c+=1
            print(f"=========  {c}  ========")
            self.create_user_with_roles(user, [random.choice(roles)])
            
      
    def get_users_with_role(self, primaryRoleType):
        print(f"user?primaryRoleType={primaryRoleType.value}")
        resp, code = self.api.get(f"user?primaryRoleType={primaryRoleType.value}")
        return resp, code
        # return resp.json(), code
    # def create_users(self, users):
    #     created_users = []
    #     print(f"Creating {len(users)} users:")
    #     for user in users:
    #         created, code = self.create_user(user)
    #         if code == 201:
    #             created_users.append(created)
    #     if len(created_users) < len(users):
    #         print(f"ERROR: Could only create {len(users)} users.")