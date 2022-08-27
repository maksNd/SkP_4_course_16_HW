from main import app
from bp_users.bp_users import bp_users

app.register_blueprint(bp_users)

if __name__ == '__main__':
    app.run()