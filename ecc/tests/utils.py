from . import factories


def login(client, user=None):
    """
    Log a user in for the given test session.
    """
    if not user:
        user = factories.UserFactory(password='123')
    login_success = client.login(username=user.email, password='123')
    assert login_success
    return user
