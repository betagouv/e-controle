from ecc import settings
from django.contrib.auth.models import User

class AdUserBackend:
  """

  """

  def authenticate(self, request, username, password):
    pass

  def get_user(self, email):
    try:
      return User.object.get(email=email)
    except User.DoesNotExist:
      return None
