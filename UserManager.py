import csv
import os
from librarian import Librarian
from regular_user import RegularUser

class UserManager:
    def __init__(self, filename="MembersData.csv"):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = []
        if os.path.exists(self.filename):
            with open(self.filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Role'] == 'librarian':
                        user = Librarian(
                            user_id=row['User-ID'],
                            name=row['Name'],
                            age=row['Age'],
                            email=row['Email'],
                            password=row['Password']
                        )
                    else:
                        user = RegularUser(
                            user_id=row['User-ID'],
                            name=row['Name'],
                            age=row['Age'],
                            email=row['Email'],
                            password=row['Password']
                        )
                    users.append(user)
        return users

    def save_users(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['User-ID', 'Name', 'Age', 'Email', 'Password', 'Role']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for user in self.users:
                writer.writerow({
                    'User-ID': user.user_id,
                    'Name': user.name,
                    'Age': user.age,
                    'Email': user.email,
                    'Password': user.password,
                    'Role': user.role
                })

    def login(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None

    def register_user(self, name, age, email, password, role="user"):
        for user in self.users:
            if user.email == email:
                return False, "Email already exists"

        new_id = 1
        if self.users:
            new_id = max(int(u.user_id) for u in self.users) + 1

        if role == 'librarian':
            new_user = Librarian(new_id, name, age, email, password)
        else:
            new_user = RegularUser(new_id, name, age, email, password)

        self.users.append(new_user)
        self.save_users()
        return True, "Registered successfully"