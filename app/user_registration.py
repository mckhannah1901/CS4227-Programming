from app import Person, db, models, interceptor_manager


def register_new_user(first_name, last_name, email, username, password):
    person_builder = models.PersonBuilder()
    person_builder.set_variables(username, email, password, first_name, last_name)

    person_manager = models.PersonManager()
    person_manager.set_builder(person_builder)

    person = person_manager.get_person()

    email_exists = db.session.query(Person.id).filter_by(email=email).first()
    username_exists = db.session.query(Person.id).filter_by(username=username).first()

    if first_name == '' or last_name == '' or email == '' or username == '' or password == '':
        interceptor_manager.execute("All fields of the form must be filled in!")
        raise Exception
    elif email_exists:
        interceptor_manager.execute("This email already exists in the database. Please choose another!")
        raise Exception
    elif username_exists:
        interceptor_manager.execute("This username already exists in the database. Please choose another!")
        raise Exception
    else:
        db.session.add(person)
        db.session.commit()
        interceptor_manager.execute("Registration completed successfully!")
