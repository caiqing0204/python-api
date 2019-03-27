import ldap

# Open a connection
l = ldap.initialize("ldap://127.0.0.1:389/")

# Bind/authenticate with a user with apropriate rights to add objects
l.simple_bind_s("cn=xxxxx,dc=xxxxxxxxxxx,dc=xxx","xxxxxxx")


## The next lines will also need to be changed to support your search requirements and directory
PeopleDN = ""
GroupDN = ""
HostGroupDN = ""

searchScope = ldap.SCOPE_SUBTREE
## retrieve all attributes - again adjust to your needs - see documentation for more options
retrieveAttributes = None
searchFilter = "(uid=wctest*)"

try:
        ldap_result = l.search_s(PeopleDN, ldap.SCOPE_SUBTREE, query)
        print ldap_result
except ldap.LDAPError, e:
        print e
