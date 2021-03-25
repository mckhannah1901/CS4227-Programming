from app import Person, db


def register_new_user(first_name, last_name, email, username, password):
    registration = Person(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

    email_exists = db.session.query(Person.id).filter_by(email=email).first()
    username_exists = db.session.query(Person.id).filter_by(username=username).first()

    if first_name == '' or last_name == '' or email == '' or username == '' or password == '':
        print("All fields of the form must be filled in!")
        raise Exception
    elif email_exists:
        print("This email already exists in the database. Please choose another!")
        raise Exception
    elif username_exists:
        print("This username already exists in the database. Please choose another!")
        raise Exception
    else:
        db.session.add(registration)
        db.session.commit()
        print("Registration completed successfully!")
