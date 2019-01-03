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
