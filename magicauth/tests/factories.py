from django.contrib.auth import get_user_model

import factory
from faker import Factory as FakerFactory

from pytest_factoryboy import register

faker = FakerFactory.create('fr_FR')


@register
class UserFactory(factory.DjangoModelFactory):
    first_name = factory.LazyFunction(faker.first_name)
    last_name = factory.LazyFunction(faker.last_name)
    email = factory.LazyFunction(faker.email)
    username = factory.LazyAttribute(lambda a: a.email)
    password = factory.PostGenerationMethodCall('set_password', '123')
    is_active = True
    is_staff = True

    class Meta:
        model = get_user_model()


@register
class MagicTokenFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'magicauth.MagicToken'
