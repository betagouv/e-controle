from django.urls.exceptions import NoReverseMatch
from pytest import mark, raises
from rest_framework.test import APIClient

from control.models import Questionnaire
from tests import factories, utils

pytestmark = mark.django_db
client = APIClient()


def get_theme(user, id):
    return utils.get_resource(client, user, 'theme', id)


def update_theme(user, payload):
    return utils.update_resource(client, user, 'theme', payload)


def delete_theme(user, payload):
    return utils.delete_resource(client, user, 'theme', id)


def make_update_theme_payload(theme):
    return {
        "id": str(theme.id),
        "title": theme.title
    }


def test_can_access_theme_api_if_control_is_associated_with_the_user():
    theme = factories.ThemeFactory()
    user = utils.make_audited_user(theme.questionnaire.control)
    assert update_theme(user, make_update_theme_payload(theme)).status_code == 200


def test_no_access_to_theme_api_if_control_is_not_associated_with_the_user():
    theme_in = factories.ThemeFactory()
    theme_out = factories.ThemeFactory()
    user = utils.make_audited_user(theme_in.questionnaire.control)
    assert update_theme(user, make_update_theme_payload(theme_out)).status_code != 200


def test_no_access_to_theme_api_for_anonymous():
    theme = factories.ThemeFactory()
    response = utils.get_resource_without_login(client, 'theme', theme.id)
    assert response.status_code == 403


def test_can_update_theme_order():
    theme = factories.ThemeFactory()
    user = utils.make_audited_user(theme.questionnaire.control)
    original_order = theme.order
    new_order = 123
    assert new_order != original_order

    payload = {
        "id": str(theme.id),
        "order": str(new_order),
        "title": theme.title
    }

    response = utils.update_resource(client, user, 'theme', payload)

    assert response.status_code == 200
    assert response.data['order'] == new_order


def test_no_access_to_theme_for_deleted_control():
    theme = factories.ThemeFactory()
    user = utils.make_audited_user(theme.questionnaire.control)
    theme.questionnaire.control.delete()
    assert update_theme(user, make_update_theme_payload(theme)).status_code == 404


def test_cannot_list_themes():
    with raises(NoReverseMatch):
        utils.list_resource_without_login(client, 'theme')


def test_cannot_retrieve_theme_even_if_user_belongs_to_control():
    theme = factories.ThemeFactory()
    audited_user = utils.make_audited_user(theme.questionnaire.control)
    inspector_user = utils.make_inspector_user(theme.questionnaire.control)
    assert not theme.questionnaire.is_draft

    assert get_theme(audited_user, theme.id).status_code == 405
    assert get_theme(inspector_user, theme.id).status_code == 405


def test_audited_cannot_retrieve_theme_from_draft_questionnaire():
    theme = factories.ThemeFactory()
    audited_user = utils.make_audited_user(theme.questionnaire.control)
    theme.questionnaire.is_draft = True
    theme.questionnaire.save()
    assert Questionnaire.objects.get(id=theme.questionnaire.id).is_draft

    assert get_theme(audited_user, theme.id).status_code == 405


def test_cannot_delete_theme_even_if_user_belongs_to_control():
    theme = factories.ThemeFactory()
    audited_user = utils.make_audited_user(theme.questionnaire.control)
    inspector_user = utils.make_inspector_user(theme.questionnaire.control)
    assert not theme.questionnaire.is_draft

    assert delete_theme(audited_user, theme.id).status_code == 405
    assert delete_theme(inspector_user, theme.id).status_code == 405


def test_audited_cannot_delete_theme_from_draft_questionnaire():
    theme = factories.ThemeFactory()
    audited_user = utils.make_audited_user(theme.questionnaire.control)
    theme.questionnaire.is_draft = True
    theme.questionnaire.save()
    assert Questionnaire.objects.get(id=theme.questionnaire.id).is_draft

    assert delete_theme(audited_user, theme.id).status_code == 405
