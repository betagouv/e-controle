from django.shortcuts import reverse
from pytest import mark
from rest_framework.test import APIClient

from control.models import Control
from tests import factories, utils

pytestmark = mark.django_db
client = APIClient()


### Get is disabled. It should never work.

def get_control(user, id):
    return utils.get_resource(client, user, 'control', id)


def test_cannot_get_control_even_if_control_is_associated_with_the_user():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    assert get_control(user, control.id).status_code == 405


def test_cannot_get_control_if_control_is_not_associated_with_the_user():
    control_in = factories.ControlFactory()
    control_out = factories.ControlFactory()
    user = utils.make_audited_user(control_in)
    assert get_control(user, control_out.id).status_code == 405


def test_cannot_get_control_for_anonymous():
    control = factories.ControlFactory()
    response = utils.get_resource_without_login(client, 'control', control.id)
    assert response.status_code == 403


def test_cannot_get_deleted_control():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    control.delete()
    assert get_control(user, control.id).status_code == 405


### List
def list_control(user):
    return utils.list_resource(client, user, 'control')


def test_inspector_can_list_controls():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    assert list_control(user).status_code == 200


def test_audited_can_list_controls():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    assert list_control(user).status_code == 200


def test_draft_questionnaire_is_not_listed_in_controls_data_if_user_is_audited():
    control = factories.ControlFactory()
    factories.QuestionnaireFactory(control=control, is_draft=False, title='MUST BE LISTED')
    factories.QuestionnaireFactory(control=control, is_draft=True, title='MUST NOT BE LISTED')
    user = utils.make_audited_user(control)
    response = list_control(user)
    assert response.status_code == 200
    assert 'MUST BE LISTED' in str(response.content)
    assert 'MUST NOT BE LISTED' not in str(response.content)


### Create
def create_control(user, payload):
    return utils.create_resource(client, user, 'control', payload)


def make_create_payload():
    return {
        "title": "new control",
        "reference_code": "ABC_2019",
    }


def test_can_access_control_create_api_if_inspector_user():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    assert create_control(user, make_create_payload()).status_code == 201


def test_cannot_create_control_with_special_characters_in_reference_code():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    data = make_create_payload()
    data['reference_code'] = 'this/is/not/good!'
    assert create_control(user, data).status_code == 400


def test_no_access_to_control_create_api_if_not_inspector():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    assert create_control(user, make_create_payload()).status_code == 403


def test_no_access_to_control_create_api_for_anonymous():
    payload = make_create_payload()
    response = utils.create_resource_without_login(client, 'control', payload)
    assert response.status_code == 403


def test_creates_control_and_adds_to_current_user():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    payload = make_create_payload()
    response = create_control(user, payload)
    response_control = response.data

    # Response data
    assert response_control['title'] == payload['title']
    assert response_control['reference_code'] == payload['reference_code']

    # Saved data
    saved_control = Control.objects.get(id=response_control['id'])
    assert saved_control.title == payload['title']
    assert saved_control.reference_code == payload['reference_code']
    assert user.profile.controls.all().get(id=response_control['id']) == saved_control


### Update

def update_control(user, payload, control):
    utils.login(client, user=user)
    url = reverse('api:control-detail', args=[control.id])
    response = client.put(url, payload, format='json')
    return response


def make_update_payload():
    return {
        "title": "updated control",
        "depositing_organization": "updated organization",
    }


def test_can_access_control_update_api_if_inspector_user():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    assert update_control(user, make_update_payload(), control).status_code == 200


def test_no_access_to_control_update_api_if_not_inspector():
    control = factories.ControlFactory()
    user = utils.make_audited_user(control)
    assert update_control(user, make_update_payload(), control).status_code == 403


def test_inspector_cannot_update_a_control_that_does_not_belong_to_him():
    control1 = factories.ControlFactory()
    control2 = factories.ControlFactory()
    user = utils.make_inspector_user(control2)
    assert update_control(user, make_update_payload(), control1).status_code == 404


def test_no_access_to_control_update_api_for_anonymous():
    control = factories.ControlFactory()
    url = reverse('api:control-detail', args=[control.id])
    response = client.put(url, make_update_payload(), format='json')
    assert response.status_code == 403


def test_no_access_to_control_update_api_if_deleted():
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    control.delete()
    assert update_control(user, make_update_payload(), control).status_code == 404


## Delete is never allowed

def test_cannot_delete_a_control():
    """
    This is a testing the DELETE method that should not be allowed.
    To remove a contrl, we do a soft delete.
    """
    control = factories.ControlFactory()
    user = utils.make_inspector_user(control)
    count_before = Control.objects.active().count()

    response = utils.delete_resource(client, user, 'control', control.pk)

    count_after = Control.objects.active().count()
    assert count_before == count_after
    assert response.status_code == 405

## Get users of a control


def get_users_of_control(current_user, control):
    utils.login(client, user=current_user)
    url = reverse('api:control-users', args=[control.id])
    return client.get(url)


def test_can_get_users_of_control_if_control_belongs_to_user():
    control = factories.ControlFactory()
    inspector = utils.make_inspector_user(control)
    audited = utils.make_audited_user(control)

    assert get_users_of_control(inspector, control).status_code == 200
    assert get_users_of_control(audited, control).status_code == 200


def test_cannot_get_users_of_control_if_control_does_not_belong_to_user():
    control = factories.ControlFactory()
    inspector = utils.make_inspector_user()
    audited = utils.make_audited_user()

    assert get_users_of_control(inspector, control).status_code == 404
    assert get_users_of_control(audited, control).status_code == 404


def test_cannot_get_users_of_neigboring_control():
    # testing for a specific bug we had.
    control_1 = factories.ControlFactory()
    inspector_1 = utils.make_inspector_user(control_1)

    control_2 = factories.ControlFactory()
    inspector_2 = utils.make_inspector_user(control_2)
    inspector_2.profile.controls.add(control_1)

    # control_2 is unknown to inspector_1.
    # inspector_2 is known to inspector_1/
    # So inspector_1 should not be able to get info on control_2.

    assert get_users_of_control(inspector_1, control_2).status_code == 404


def test_cannot_get_users_of_control_if_control_is_deleted():
    control = factories.ControlFactory()
    inspector = utils.make_inspector_user(control)
    audited = utils.make_audited_user(control)
    control.delete()

    assert get_users_of_control(inspector, control).status_code == 404
    assert get_users_of_control(audited, control).status_code == 404
