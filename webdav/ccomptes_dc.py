from __future__ import print_function

from ldap3 import Server, Connection, ALL, NTLM
from wsgidav import compat, util
from wsgidav.dc.base_dc import BaseDomainController
from ecc import settings
from control.models import Control
from django.contrib.auth.models import User


class CCDomainController(BaseDomainController):

    def __init__(self, wsgidav_app, config):
        super(CCDomainController, self).__init__(wsgidav_app, config)
        ## TODO: add configuration

    def get_domain_realm(self, path_info, environ):
        """Return the normalized realm name for a given URL.

        This method is called

        - On startup, to check if anonymous access is allowed for a given share.
        In this case, `environ` is None.
        - For every request, before basic or digest authentication is handled.

        A domain controller that uses the share path as realm name may use
        the `_calc_realm_from_path_provider()` helper.

        Args:
        path_info (str):
        environ (dict | None):
        Returns:
        str
        """
        # we only send the control code
        realms = list(filter(None, path_info.split('/')))
        if len(realms) != 0:
            return realms[0]
        else:
            return ""


    def require_authentication(self, realm, environ):
        """Return False to disable authentication for this request.

        This method is called

        - On startup, to check if anonymous access is allowed for a given share.
        In this case, `environ` is None.
        - For every request, before basic or digest authentication is handled.
        If False is returned, we MAY also set environment variables for
        anonymous access::

            environment["wsgidav.auth.roles"] = (<role>, ...)
            environment["wsgidav.auth.permissions"] = (<perm>, ...)
            return False

        Args:
        realm (str):
        environ (dict | None):
        Returns:
        False to allow anonymous access
        True to force subsequent digest or basic authentication
        """
        #print("require auth test")
        return True

    def basic_auth_user(self, realm, user_name, password, environ):
        """Check request access permissions for realm/user_name/password.

        Called by http_authenticator for basic authentication requests.

        Optionally set environment variables:

        environ["wsgidav.auth.roles"] = (<role>, ...)
        environ["wsgidav.auth.permissions"] = (<perm>, ...)

        Args:
        realm (str):
        user_name (str):
        password (str):
        environ (dict):
        Returns:
        False if user is not known or not authorized
        True if user is authorized
        """

        ##Todo add verification corresponding to the given user
        username = environ['REMOTE_USER']
        username = username.split('@', 1)[0]

        # We know that the following user exists in the LDAP
        # We now check the realm
        try:
            user = User.objects.get(profile__active_directory_name=username)
            environ["wsgidav.auth.roles"] = ("reader")
            if user.profile.controls.filter(reference_code=realm).exists() or realm == "":
                return True
        except Exception as e:
            print(e)
            return False

    def supports_http_digest_auth(self):
        """Signal if this DC instance supports the HTTP digest authentication theme.

        If true, `HTTPAuthenticator` will call `dc.digest_auth_user()`,
        so this method must be implemented as well.

        Returns:
        bool
        """
        print("supports http test")
        return False 

    def digest_auth_user(self, realm, user_name, environ):
        pass
        """Check access permissions for realm/user_name.

        Called by http_authenticator for basic authentication requests.

        Compute the HTTP digest hash A1 part.

        Any domain controller that returns true for `supports_http_digest_auth()`
        MUST implement this method.

        Optionally set environment variables:

            environ["wsgidav.auth.roles"] = (<role>, ...)
            environ["wsgidav.auth.permissions"] = (<perm>, ...)

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
        # user = self._get_realm_entry(realm, user_name)
        # user = {'password': 'test', 'roles': ['editor']}
        # if user is None:
        #     return False
        # password = user.get("password")
        # environ["wsgidav.auth.roles"] = user.get("roles", [])
        # return self._compute_http_digest_a1(realm, user_name, password)
