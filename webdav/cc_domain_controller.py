from __future__ import print_function
from ecc import settings
from django.contrib.auth.models import User
from ldap3 import Server, Connection, ALL, NTLM
import logging
from wsgidav.dc.base_dc import BaseDomainController


class CCDomainController(BaseDomainController):
  """
  This domain controller grants access to requested URIs based on the permissions associated to the
  Django user. If fetches the corresponding Django user and queries the DJango ORM to know if user
  should have access.
  """

  def __init__(self, wsgidav_app, config):
    super(CCDomainController, self).__init__(wsgidav_app, config)

  def get_domain_realm(self, path_info, environ):
    """Return the normalized realm name for a given URL.

    This method is called

    - On startup, to check if anonymous access is allowed for a given share.
    In this case, `environ` is None.
    - For every request, before basic or digest magicauth is handled.

    A domain controller that uses the share path as realm name may use
    the `_calc_realm_from_path_provider()` helper.

    Args:
    path_info (str):
    environ (dict | None):
    Returns:
    str
    """
    logging.debug('Get domain realm: Start')
    if environ is not None:
      # Pretend that the incoming request uses Basic authentication HTTP header, because it's easier
      # to make it work with wsgidav.
      # (see https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
      # Since Apache passes vars through environment variable, we write an environment variable to
      # imitate a HTTP Authorization header with Basic.
      # TODO : make kerberos requests work (instead of prentending the requests are Basic)
      environ['HTTP_AUTHORIZATION'] = settings.HTTP_AUTHORIZATION

    # We return the realm, which corresponds to the control reference_code.
    # Example : path_info = '2020_control_of_the_city/Q01/T01/Q01-T01-03-important_document.pdf'
    # The realm is : '2020_control_of_the_city'
    realms = list(filter(None, path_info.split('/')))
    if len(realms) != 0:
      return realms[0]
    else:
      # The root ("/") has been requested
      return ""


  def require_authentication(self, realm, environ):
    """Return False to disable magicauth for this request.

    This method is called

    - On startup, to check if anonymous access is allowed for a given share.
    In this case, `environ` is None.
    - For every request, before basic or digest magicauth is handled.
    If False is returned, we MAY also set environment variables for
    anonymous access::

        environment["wsgidav.magicauth.roles"] = (<role>, ...)
        environment["wsgidav.magicauth.permissions"] = (<perm>, ...)
        return False

    Args:
    realm (str):
    environ (dict | None):
    Returns:
    False to allow anonymous access
    True to force subsequent digest or basic magicauth
    """
    return True

  def basic_auth_user(self, realm, user_name, password, environ):
    """Check request access permissions for realm/user_name/password.

    Called by http_authenticator for basic magicauth requests.

    Optionally set environment variables:

    environ["wsgidav.magicauth.roles"] = (<role>, ...)
    environ["wsgidav.magicauth.permissions"] = (<perm>, ...)

    Args:
    realm (str): In this case the realm is equal to the control code or ab empty string
    user_name (str):
    password (str):
    environ (dict):
    Returns:
    False if user is not known or not authorized
    True if user is authorized
    """
    logging.debug('Start basic magicauth user')

    def get_samaccount_from_env(environ):
      """
      The format for REMOTE_USER is samaccount@CCOMPTES.FR.
      Example : for Caroline Elbourki : celbourki@CCOMPTES.fr
      The REMOTE_USER environment variable was set by the webserver.
      """
      username = environ['REMOTE_USER']
      samaccount = username.split('@', 1)[0]
      return samaccount

    def get_email_from_samacount(samaccount):
      """
      Query the LDAP server (e.g. Active Directory) to get the email of the user corresponding to
      the samaccount.
      Raise exception if not found.
      TODO : create proper exception classes extending Exception
      """
      logging.info(f'Basic magicauth: LDAP Sever (samaccount: {samaccount})')
      server = Server(settings.LDAP_SERVER, get_info=ALL)
      conn = Connection(server, user=settings.LDAP_DOMAIN + "\\" + settings.LDAP_USER,
                        password=settings.LDAP_PASSWORD, authentication=NTLM)
      logging.debug('Basic magicauth: LDAP Binding')

      if conn.bind():
        conn.search(settings.LDAP_DC,
                    f'(&(objectClass=user)(sAMAccountName={samaccount}))',
                    attributes=['mail'])
        logging.debug('Basic magicauth: LDAP search')
        if len(conn.entries) == 1:
          email = conn.entries[0].mail.value
          return email
        elif len(conn.entries) == 0:
          raise Exception(f"sAMAccount name {samaccount} not found in LDAP server")
        else:
          raise Exception(f"sAMAccount name has several email addresses linked to.({samaccount})")
      else:
        raise Exception(f"Cannot access LDAP server ({settings.LDAP_SERVER})")

    def get_django_user_from_email(email):
      """
      Use the Django ORM to fetch the user object corresponding to this email.
      """
      user = User.objects.get(username=email.lower())
      return user

    def can_user_access_realm(django_user, realm):
      """
      Check if the django user has access to the control corresponding to the realm.
      The realm in our case is the directory where the control's files are, which is
      control.reference_code
      """
      # The request is readonly (files should never be edited)
      environ["wsgidav.magicauth.roles"] = ("reader")
      # TODO : isolate case realm == "", it was necessary for windows 7 only
      if django_user.profile.controls.filter(reference_code=realm).exists() or realm == "":
        return True
      return False

    samaccount = get_samaccount_from_env(environ)
    try:
      email = get_email_from_samacount(samaccount)
      user = get_django_user_from_email(email)
      return can_user_access_realm(user, realm)
    except Exception as e:
      logging.error(e)
      return False


  def supports_http_digest_auth(self):
    """Signal if this DC instance supports the HTTP digest magicauth theme.

    If true, `HTTPAuthenticator` will call `dc.digest_auth_user()`,
    so this method must be implemented as well.

    Returns:
    bool
    """
    return False

  def digest_auth_user(self, realm, user_name, environ):
    """Check access permissions for realm/user_name.

    Called by http_authenticator for basic magicauth requests.

    Compute the HTTP digest hash A1 part.

    Any domain controller that returns true for `supports_http_digest_auth()`
    MUST implement this method.

    Optionally set environment variables:

        environ["wsgidav.magicauth.roles"] = (<role>, ...)
        environ["wsgidav.magicauth.permissions"] = (<perm>, ...)

    Note that in order to calculate A1, we need either

    - Access the plain text password of the user.
      In this case the method `self._compute_http_digest_a1()` can be used
      for convenience.
      Or

    - Return a stored hash value that is associated with the user name
      (for example from Apache's htdigest files).

    Args:
        realm (str):
        user_name (str):
        environ (dict):

    Returns:
        str: MD5("{usern_name}:{realm}:{password}")
        or false if user is unknown or rejected
    """
    pass
