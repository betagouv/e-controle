import importlib
import sys

from django.conf import settings
from django.shortcuts import reverse
from django.urls import clear_url_caches
from user_profiles.models import UserProfile

from . import factories


def login(client, user=None):
    """
    Log a user in for the given test session.
    """
    if not user:
        user = factories.UserFactory()
    user.set_password('123')
    user.save()
    login_success = client.login(username=user.username, password='123')
    assert login_success
    return user


def reload_urlconf():
    """
    Sometimes, you need to reload Django URLs, for instance if you change
    some settings right in your tests.
    """
    clear_url_caches()
    urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        importlib.reload(sys.modules[urlconf])


def make_user(profile_type, control=None, assign_questionnaire_editor=True):
    user_profile = factories.UserProfileFactory(profile_type=profile_type)
    if control is not None:
        user_profile.controls.add(control)
        if assign_questionnaire_editor:
            control.questionnaires.update(editor=user_profile.user)
    user_profile.save()
    return user_profile.user


def make_audited_user(control=None):
    return make_user(UserProfile.AUDITED, control)


def make_inspector_user(control=None, assign_questionnaire_editor=True):
    return make_user(
        UserProfile.INSPECTOR, control, assign_questionnaire_editor=assign_questionnaire_editor)


def get_resource(client, user, resource_type, resource_id):
    """
    Call the rest api for the resource.
    :param client: APIClient
    :param user: user to log in
    :param resource_type: e.g. 'questionnaire'
    :param resource_id: e.g. 32
    :return: response object from API
    """
    login(client, user=user)
    return get_resource_without_login(client, resource_type, resource_id)


def get_resource_without_login(client, resource_type, resource_id):
    url = reverse('api:' + resource_type + '-detail', args=[resource_id])
    response = client.get(url)
    return response


def create_resource(client, user, resource_type, payload):
    """
    Call the rest api to create a resource.
    :param client: APIClient
    :param user: user to log in
    :param resource_type: e.g. 'questionnaire'
    :param payload: e.g. {"title": "Cool questionnaire"}
    :return: response object from API
    """
    login(client, user=user)
    return create_resource_without_login(client, resource_type, payload)


def create_resource_without_login(client, resource_type, payload):
    url = reverse('api:' + resource_type + '-list')
    response = client.post(url, payload, format='json')
    return response


def update_resource(client, user, resource_type, payload):
    """
    Call the rest api to update a resource.
    :param client: APIClient
    :param user: user to log in
    :param resource_type: e.g. 'questionnaire'
    :param payload: Should contain an id. e.g. {"id": 123, "title": "Cool questionnaire"}
    :return: response object from API
    """
    login(client, user=user)
    return update_resource_without_login(client, resource_type, payload)


def update_resource_without_login(client, resource_type, payload):
    url = reverse('api:' + resource_type + '-detail', args=[payload['id']])
    response = client.put(url, payload, format='json')
    return response


def delete_resource(client, user, resource_type, resource_id):
    """
    Call the rest api to delete a resource.
    :param client: APIClient
    :param user: user to log in
    :param resource_type: e.g. 'questionnaire'
    :param resource_id: e.g. 32
    :return: response object from API
    """
    login(client, user=user)
    return delete_resource_without_login(client, resource_type, resource_id)


def delete_resource_without_login(client, resource_type, resource_id):
    url = reverse('api:' + resource_type + '-detail', args=[resource_id])
    response = client.delete(url)
    return response


def list_resource(client, user, resource_type):
    """
    Call the rest api to list all objects of a resource.
    :param client: APIClient
    :param user: user to log in
    :param resource_type: e.g. 'questionnaire'
    :return: response object from API
    """
    login(client, user=user)
    return list_resource_without_login(client, resource_type)


def list_resource_without_login(client, resource_type):
    url = reverse('api:' + resource_type + '-list')
    response = client.get(url)
    return response
