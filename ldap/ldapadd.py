# import needed modules
import ldap
import ldap.modlist as modlist

# Open a connection
l = ldap.initialize("ldap://127.0.0.1:389/")

# Bind/authenticate with a user with apropriate rights to add objects
l.simple_bind_s("cn=xxxx,dc=xxxxxxx,dc=xxx","xxxxxxxxxxx")

# The dn of our new entry/object
dn="uid=wctest,ou=xxxxxxxx,dc=xxxxxxxxxx,dc=xxx"

# A dict to help build the "body" of the object
attrs = {}
attrs['objectclass'] = ['top','shadowAccount','posixAccount','inetOrgPerson']
attrs['cn'] = 'wctest2'
attrs['userPassword'] = 'aDifferentSecret'
attrs['description'] = 'User object for replication using slurpd'
attrs['homeDirectory'] = '/home/wctest'
# Convert our dict to nice syntax for the add-function using modlist-module
ldif = modlist.addModlist(attrs)

# Do the actual synchronous add-operation to the ldapserver
l.add_s(dn,ldif)

# Its nice to the server to disconnect and free resources when done
l.unbind_s()
