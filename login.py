import os
from getpass import getpass

class LoginError(Exception):
    pass

class LoginManager:
    CREDENTIALS_FILE = 'credentials.txt'

    def __init__(self):
        # ensure credential file exists
        if not os.path.exists(self.CREDENTIALS_FILE):
            open(self.CREDENTIALS_FILE, 'w').close()

    def authenticate(self, username: str, password: str):
        """Return tuple (role, id) if success otherwise raise LoginError"""
        try:
            with open(self.CREDENTIALS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('|')
                    if len(parts) < 3:
                        continue
                    u, p, role = parts[0], parts[1], parts[2]
                    sid = parts[3] if len(parts) > 3 else ''
                    if u == username and p == password:
                        return role, sid
            raise LoginError('Invalid username or password')
        except FileNotFoundError:
            raise LoginError('Credentials file missing')

    def change_password(self, username: str):
        """Change password for username in credentials file"""
        old = getpass('Enter current password: ')
        try:
            # validate old password
            role_sid = self.authenticate(username, old)
        except LoginError as e:
            print('Authentication failed:', e)
            return False

        new = getpass('Enter new password: ')
        confirm = getpass('Confirm new password: ')
        if new != confirm:
            print('Passwords do not match')
            return False

        lines = []
        changed = False
        with open(self.CREDENTIALS_FILE, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line:
                    continue
                parts = line.split('|')
                if parts[0] == username:
                    parts[1] = new
                    changed = True
                lines.append('|'.join(parts))
        if changed:
            with open(self.CREDENTIALS_FILE, 'w') as f:
                for ln in lines:
                    f.write(ln + '\n')
            print('Password changed successfully')
            return True
        else:
            print('User not found')
            return False

    def register_student(self, username, password, student_id):
        # Utility: add a student credential
        with open(self.CREDENTIALS_FILE, 'a') as f:
            f.write(f"{username}|{password}|student|{student_id}\n")


