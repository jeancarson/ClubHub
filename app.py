from application import app
from application.util.db_functions import get_users_info, approve_user


# DARRAGH – TODO: Fix styles overriding each other and add navbar to admin pages

with app.app_context():

    # MIA! You can use this to get all rows of "PENDING" users:
    unapproved_users = get_users_info(unapproved=True, admin_permission=True)

    # # Approve all the users
    # for user in unapproved_users:
    #     approve_user(user_id=user["user_id"])
    #approve_user(user_id=6)

if __name__ == '__main__':
    app.run()
