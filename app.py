from application import app
# from application.util.db_functions.users import *

# You can use this to get all rows of "PENDING" users:
# ====================================================
# from util.db_functions.users import get_users_info, approve_user
#
# unapproved_users = get_users_info(pending=True, admin_permission=True)
#

# Approve all the users
# =====================
# for user in unapproved_users:
#     approve_user(user_id=user["user_id"])
#

# TODO: "Delete my account button on profile"


if __name__ == '__main__':
    app.run()
