from database import Database
# Note Please Dont add duplicate admin user
# This script is used to add a new admin user to the database
# change the username and password as per your requirement
def add_admin_user(username, password):
    db = Database()
    db.insert_admin(username, password)
    print(f"Admin user '{username}' added successfully.")

if __name__ == '__main__':
    add_admin_user('admin', 'admin')  # Add a default admin user
