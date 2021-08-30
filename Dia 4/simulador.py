from faker import Faker
from faker.providers import person,misc

fake=Faker()
fake.add_provider(person)
fake.add_provider(misc)
print(fake.name())
print(fake.first_name_male())
print(fake.first_name_female())
print(fake.uuid4())