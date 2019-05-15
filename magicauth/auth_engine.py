from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User
from ecc import settings
from ldap3 import Server, Connection, NTLM, ALL
import logging


class TunedRemoteUserBackend(RemoteUserBackend):
  create_unknown_user=False

  def authenticate(self, request, remote_user):
    logging.debug(remote_user)
    username = remote_user.split('@', 1)[0] # example avalingot@CCOMPTES.FR

    try:
      logging.info(f'Basic magicauth: LDAP Sever (username: {username})')
      server = Server(settings.LDAP_SERVER, get_info=ALL)
      conn = Connection(server, user=settings.LDAP_DOMAIN + "\\" + settings.LDAP_USER,
                        password=settings.LDAP_PASSWORD, authentication=NTLM)
      logging.debug('Basic magicauth: LDAP Binding')
      if conn.bind():
        conn.search(settings.LDAP_DC,
                    f'(&(objectClass=user)(sAMAccountName={username}))',
                    attributes=['mail'])
        logging.debug('Basic magicauth: LDAP search')
        if len(conn.entries) == 1:
          email = conn.entries[0].mail.value
          user = User.objects.get(email=email)
          return user
        else:
          if len(conn.entries) == 0:
            raise Exception(f"sAMAccount name doesnt exist {username}")
          elif len(conn.entries) > 1:
            raise Exception(f"sAMAccount name has several email addresses linked to.({username})")
      else:
        raise Exception(f"Can't not access to Active directory server ({settings.LDAP_SERVER})")
    except Exception as e:
      logging.error(e)
      return None