# import needed modules
import ldap
import ldap.modlist as modlist

# Open a connection
l = ldap.initialize("ldap://127.0.0.1:389/")

# Bind/authenticate with a user with apropriate rights to add objects

l.simple_bind_s("cn=xxxxxxxx,dc=xxxxxxxx,dc=xxx","xxxxxx")
# The dn of our existing entry/object
dn="cn=wwww,dc=xxxxxx,dc=xxx"

# Some place-holders for old and new values
old = {'description':'User object for replication using slurpd'}
new = {'description':'Bind object used for replication using slurpd'}

# Convert place-holders for modify-operation using modlist-module
ldif = modlist.modifyModlist(old,new)

# Do the actual modification
l.modify_s(dn,ldif)

# Its nice to the server to disconnect and free resources when done
l.unbind_s()

