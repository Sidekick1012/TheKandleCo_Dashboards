"""
Simple script to add new users to PostgreSQL database
"""

import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from login import add_user

def main():
    print("="*50)
    print("Add New User to Database")
    print("="*50)
    
    # Get username
    username = input("\nEnter username: ").strip()
    if not username:
        print("[-] Username cannot be empty!")
        return
    
    # Get password
    password = input("Enter password: ").strip()
    if not password:
        print("[-] Password cannot be empty!")
        return
    
    # Confirm password
    password_confirm = input("Confirm password: ").strip()
    if password != password_confirm:
        print("[-] Passwords don't match!")
        return
    
    # Add user
    print("\n[*] Adding user to database...")
    success, message = add_user(username, password)
    
    if success:
        print(f"[+] {message}")
        print(f"[+] User '{username}' can now login!")
    else:
        print(f"[-] {message}")

if __name__ == "__main__":
    main()
