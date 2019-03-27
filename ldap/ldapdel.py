import ldap

## first you must bind so we're doing a simple bind first
try:
	l = ldap.open("127.0.0.1")

	l.protocol_version = ldap.VERSION3
	# Pass in a valid username and password to get
	# privileged directory access.
	# If you leave them as empty strings or pass an invalid value
	# you will still bind to the server but with limited privileges.

	username = "cn=xxxxxxx,dc=xxxxxxxxxxxxx,dc=xxxxxxx"
	password  = "xxxxxxxxxxxxx"

	# Any errors will throw an ldap.LDAPError exception
	# or related exception so you can ignore the result
	l.simple_bind(username, password)
except ldap.LDAPError, e:
	print e
	# handle error however you like


# The next lines will also need to be changed to support your requirements and directory
deleteDN = "cn=wwww,dc=xxxxxxxxxx,dc=xxxxx"
try:
	# you can safely ignore the results returned as an exception
	# will be raised if the delete doesn't work.
	l.delete_s(deleteDN)
except ldap.LDAPError, e:
	print e
	## handle error however you like
