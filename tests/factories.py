import factory

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from pytest_factoryboy import register
from faker import Factory as FakerFactory

faker = FakerFactory.create('fr_FR')


dummy_file = SimpleUploadedFile(
    name='test.pdf',
    content=open(settings.BASE_DIR + '/tests/data/test.pdf', 'rb').read(),
    content_type='application/pdf')


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
class UserProfileFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'user_profiles.UserProfile'


@register
class MagicTokenFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'magicauth.MagicToken'


@register
class ControlFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(faker.name)
    reference_code = 'CONTROL'

    class Meta:
        model = 'control.Control'


@register
class QuestionnaireFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(faker.name)
    control = factory.SubFactory(ControlFactory)
    file = dummy_file

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


@register
class ResponseFileFactory(factory.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)
    author = factory.SubFactory(UserFactory)
    file = dummy_file

    class Meta:
        model = 'control.ResponseFile'


@register
class QuestionFileFactory(factory.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)
    file = dummy_file

    class Meta:
        model = 'control.QuestionFile'
