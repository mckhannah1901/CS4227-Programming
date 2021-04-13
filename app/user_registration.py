from app import Person, db, models, interceptor_manager
from app.models import Log


def register_new_user(first_name, last_name, email, username, password):
    person_builder = models.PersonBuilder()
    person_builder.set_variables(username, email, password, first_name, last_name)

    person_manager = models.PersonManager()
    person_manager.set_builder(person_builder)

    person = person_manager.get_person()

    email_exists = db.session.query(Person.id).filter_by(email=email).first()
    username_exists = db.session.query(Person.id).filter_by(username=username).first()

    if first_name == '' or last_name == '' or email == '' or username == '' or password == '':
        log = Log("All fields of the form must be filled in!")
        interceptor_manager.execute(log)
        raise Exception
    elif email_exists:
        log = Log("This email already exists in the database. Please choose another!")
        interceptor_manager.execute(log)
        raise Exception
    elif username_exists:
        log = Log("This username already exists in the database. Please choose another!")
        interceptor_manager.execute(log)
        raise Exception
    else:
        db.session.add(person)
        db.session.commit()
        log = Log("Registration completed successfully!")
        interceptor_manager.execute(log)
