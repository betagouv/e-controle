from pytest import mark

from django.contrib.auth import get_user_model

from tests import factories, utils


pytestmark = mark.django_db
User = get_user_model()


def test_an_action_log_is_added_on_user_login(client):
    user = factories.UserFactory()
    count_before = user.actor_actions.filter(verb__icontains='logged in').count()
    utils.login(client, user=user)
    count_after = user.actor_actions.filter(verb__icontains='logged in').count()
    assert count_after == count_before + 1
