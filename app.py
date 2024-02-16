from application import app
from application.util.db_functions import get_users_info


# DARRAGH – TODO: Fix styles overriding each other and add navbar to admin pages

with app.app_context():

    # MIA! You can use this to get all rows of "PENDING" users:
    unapproved_users = get_users_info(unapproved=True, admin_permission=True)

    # for user in unapproved_users:
    #     print(user["username"], user["approved"])

if __name__ == '__main__':
    app.run()
