import factory

from django.contrib.auth import get_user_model

from pytest_factoryboy import register
from faker import Factory as FakerFactory


faker = FakerFactory.create('fr_FR')


@register
class UserFactory(factory.DjangoModelFactory):
    first_name = factory.LazyFunction(faker.first_name)
    last_name = factory.LazyFunction(faker.last_name)
    email = factory.LazyFunction(faker.email)
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


@register
class ControlFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(faker.name)

    class Meta:
        model = 'control.Control'


@register
class QuestionnaireFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(faker.name)
    control = factory.SubFactory(ControlFactory)

    class Meta:
        model = 'control.Questionnaire'


@register
class ThemeFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(faker.name)
    questionnaire = factory.SubFactory(QuestionnaireFactory)

    class Meta:
        model = 'control.Theme'


@register
class QuestionFactory(factory.DjangoModelFactory):
    description = factory.LazyFunction(faker.name)
    theme = factory.SubFactory(ThemeFactory)

    class Meta:
        model = 'control.Question'
