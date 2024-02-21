from faker import Faker


def fake_new_client():
    """

    :return: dictionary of fake client
    """
    fake = Faker()

    first_name = "AutoTest"
    last_name = fake.last_name()
    full_name = first_name + last_name
    ssn_or_itin = '123456789'
    email = fake.email()
    mobile_phone = fake.numerify(text='###-###-####')
    city = fake.city()
    state = 'Alaska'
    advisor_name = 'Maayan Tester1'

    return {
        "First name": first_name,
        "Last name": last_name,
        "Full name": full_name,
        "SSN / ITIN": ssn_or_itin,
        "Email": email,
        "Mobile phone": mobile_phone,
        "City": city,
        "State": state,
        "Advisor Name": advisor_name
    }


def fake_credentials():
    """

    :return: dictionary of fake credentials
    """
    faker = Faker()
    username = faker.user_name()
    password = faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return {
        "username": username,
        "password": password,
    }