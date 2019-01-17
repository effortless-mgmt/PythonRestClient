from primary_roletype import PrimaryRoleType

work_period_types = ["Storage", "Cassier", "Fork Lift", "Programmer", "Consultant", "Teaching Assistant", "Floor Manager", "Driver"]

demopassword = "SecurePassword"
def demousers():
    booker = {
                "firstName": "Booker",
                "lastName": "Doe",
                "email": "booker@example.com",
                "phone": "+4522345678",
                "userName": "booker",
                "password": demopassword,
                "primaryRole": PrimaryRoleType.BOOKER.value
            }
    client = {
                "firstName": "Client",
                "lastName": "Doe",
                "email": "client@example.com",
                "phone": "+4522345678",
                "userName": "client",
                "password": demopassword,
                "primaryRole": PrimaryRoleType.CLIENT.value
            }
    substitute = {
                "firstName": "Substitute",
                "lastName": "Doe",
                "email": "substitute@example.com",
                "phone": "+4532345678",
                "userName": "substitute",
                "password": demopassword,
                "primaryRole": PrimaryRoleType.SUBSTITUTE.value
            }
    return [booker, client, substitute]

def demoroles():
    # return ["booker", "client", "substitute"]
    return [
        {
            "name": "booker",
        },
        {
            "name": "client",
        },
        {
            "name": "substitute",
        },
    ]
    # admin = {
    #     "role": {
    #         "name": "admin"
    #     }, "privileges": [
    #         "list_user",
    #         "del_user",
    #         "update_user",
    #     ]
    # }

    # client = {
    #     "role": {
    #         "name": "client"
    #     }, "privileges": [
    #         "manage_own_company"
    #     ]
    # }

    # substitute = {
    #     "role": {
    #         "name": "substitute"
    #     }, "privileges": [
    #         "list_own_appointments"
    #     ]
    # }

    # return [admin, client, substitute]
