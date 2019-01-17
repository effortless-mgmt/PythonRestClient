import sys
from api import EffortlessApi

class RoleManager:
    def __init__(self, api):
        self.api = api
        self.created_roles = []
        self.created_perms = []
    
    def create_role(self, role):
        dupes = RoleManager.find_with_name(role['name'], self.created_roles)
        if (len(dupes) > 0):
            print(f"Duplicate role {role['name']}")
            return dupes[0], 200

        print(f"- Creating role {role['name']}... ", end="")
        created, code = self.api.post("role", role)

        self.created_roles.append(created)

        return created, code

    def create_privilege(self, privilege):
        dupes = RoleManager.find_with_name(privilege['name'], self.created_perms)
        if (len(dupes) > 0):
            print(f"Duplicate privilege {privilege['name']}")
            return dupes, 200

        print(f"- Creating privilege {privilege['name']}... ", end="")
        created, code = self.api.post("privilege", privilege)

        self.created_perms.append(created)

        return created, code
    
    def find_with_name(name, lst):
        return [x for x in lst if x['name'] == name]
    
    def assign_priv_to_role(self, priv_id, role_id):
        print(f"- Assigning privilege {priv_id} to role {role_id}", end="")
        created, code = self.api.post(f"role/{role_id}/privilege/{priv_id}")
        return created, code
    
    def assign_role_to_user(self, role_id, username):
        print(f"- Assigning role {role_id} to user {username}", end="")
        created, code = self.api.post(f"user/{username}/role/{role_id}")
        return created, code

    def create_role_with_privs(self, role, privileges):
        print(f"Creating role {role['name']} with {len(privileges)} privileges:", end="")
        created_role, code = self.create_role(role)

        if code != 200 and code != 201:
            print("Failed to create role, try again.")
            return created_role, code

        for privilege in privileges:
            p = self.create_privilege(privilege)
            if p != 200 and p != 201:
                print(f"   Failed to create privilege {p['name']}")
                continue
            ap = self.assign_priv_to_role(p['id'], created_role['id'])
        
        created, code = self.api.get(f"role/{created_role['id']}")
        return created, code
