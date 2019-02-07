import factory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from pytest_factoryboy import register
from faker import Factory as FakerFactory


faker = FakerFactory.create('fr_FR')


@register
class UserFactory(factory.DjangoModelFactory):
    first_name = factory.LazyFunction(faker.first_name)
    last_name = factory.LazyFunction(faker.last_name)
    email = factory.LazyAttribute(lambda a: f'{a.first_name}.{a.last_name}@{faker.word()}.com')
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


@register
class ControlFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(lambda: f'Controle: {faker.sentence(nb_words=3)}')
    reference_code = factory.Sequence(lambda n: f'CONTROLE-{n}')

    class Meta:
        model = 'control.Control'


@register
class QuestionnaireFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(lambda: f'Questionnaire à propos de {faker.name()}')
    control = factory.SubFactory(ControlFactory)
    file = SimpleUploadedFile(
            name='test.pdf',
            content=open('./tests/data/test.pdf', 'rb').read(),
            content_type='application/pdf')

    class Meta:
        model = 'control.Questionnaire'


@register
class ThemeFactory(factory.DjangoModelFactory):
    title = factory.LazyFunction(lambda: f'Thème: {faker.name()}')
    questionnaire = factory.SubFactory(QuestionnaireFactory)

    class Meta:
        model = 'control.Theme'


@register
class QuestionFactory(factory.DjangoModelFactory):
    description = factory.LazyFunction(faker.text)
    theme = factory.SubFactory(ThemeFactory)

    class Meta:
        model = 'control.Question'


@register
class ResponseFileFactory(factory.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)
    author = factory.SubFactory(UserFactory)
    file = SimpleUploadedFile(
            name='response-file.pdf',
            content=open('./tests/data/response-file.pdf', 'rb').read(),
            content_type='application/pdf')

    class Meta:
        model = 'control.ResponseFile'


@register
class QuestionFileFactory(factory.DjangoModelFactory):
    question = factory.SubFactory(QuestionFactory)
    file = SimpleUploadedFile(
            name='annexe.xlsx',
            content=open('./tests/data/annexe.xlsx', 'rb').read(),
            content_type='application/xls')

    class Meta:
        model = 'control.QuestionFile'
