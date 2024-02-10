from application import app
# from application.util.db_functions import create_user

# # Testing
# with app.app_context():
#     create_user(username="steven", password="shitty_password", user_type="student")
#     print("Created user 'steven'!")


if __name__ == '__main__':
    app.run()
