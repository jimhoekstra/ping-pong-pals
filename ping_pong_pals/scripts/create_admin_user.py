from getpass import getpass

from ping_pong_pals.database import create_all, get_db
from ping_pong_pals.database.crud import unsafe_create_admin_user


def main() -> None:
    create_all()

    username = input("Username: ")
    password = getpass()
    password_confirm = getpass(prompt="Confirm password: ")

    if password != password_confirm:
        print("Error: passwords don't match")
        return

    db = get_db()
    try:
        unsafe_create_admin_user(db=db, username=username, password=password)

        print("Admin user successfully created!")

    finally:
        db.close()


if __name__ == "__main__":
    main()
