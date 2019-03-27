# coding:utf8
import ldap
import ldap.modlist

class Ldapapi(object):

    def __init__(self,serverip,port,username,password):
        self.con = ldap.initialize("ldap://{0}:{1}/".format(serverip,port))

        # At this point, we're connected as an anonymous user
        # If we want to be associated to an account
        # you can log by binding your account details to your connection

        self.con.simple_bind_s(username,password)

    def search(self,query,basedn):
        # query = "(uid=wctest)"
        result = self.con.search_s(basedn, ldap.SCOPE_SUBTREE, query)
        return result

    def add(self,dn,modlist):
        # dn = "uid=maarten,ou=people,dc=example,dc=com"
        # modlist = {
        #         "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount"],
        #         "uid": ["maarten"],
        #         "sn": ["De Paepe"],
        #         "givenName": ["Maarten"],
        #         "cn": ["Maarten De Paepe"],
        #         "displayName": ["Maarten De Paepe"],
        #         "uidNumber": ["5000"],
        #         "gidNumber": ["10000"],
        #         "loginShell": ["/bin/bash"],
        #         "homeDirectory": ["/home/maarten"]}
        #         }
        # addModList transforms your dictionary into a list that is conform to ldap input.
        result = self.con.add_s(dn, ldap.modlist.addModlist(modlist))

    def modifying(self,dn,old_value,new_value):
        ########## modifying (a user, or in this case, the user's password) ##########
        # this works a bit strange.
        # in a rel. database you just give the new value for the record you want to change
        # here you need to give an old/new pair

        # dn = "uid=maarten,ou=people,dc=example,dc=com"
        # # you can expand this list with whatever amount of attributes you want to modify
        # old_value = {"userPassword": ["my_old_password"]}
        # new_value = {"userPassword": ["my_new_password"]}

        modlist = ldap.modlist.modifyModlist(old_value, new_value)
        self.con.modify_s(dn, modlist)

    def delete(self,dn):
        ########## deleting (a user) #################################################
        # dn = "uid=maarten,ou=people,dc=example,cd=com"
        self.con.delete_s(dn)

if __name__ == '__main__':
    l = Ldapapi('127.0.0.1','389','cn=xxxxxxxx,dc=xxxxxxxxxxxxx,dc=xxxx','xxxxxxxxxxxxx')

    gdn = "cn=wctest8,ou=xxxxxx,dc=xxxxxxxxxxxx,dc=xx"
    gmodlist = {"objectClass": ["posixGroup","top"],
                "cn":["wctest8"],
                "gidNumber": ["90008"],
                }
    udn = "uid=wctest8,ou=xxxxxxxx,dc=xxxxxxxx,dc=xxx"
    umodlist = {
        "objectClass": ["inetOrgPerson", "posixAccount", "shadowAccount","top"],
        "uid": ["wctest8"],
        "givenName": ["wc"],
        "sn": ["test8"],
        "cn": ["wctest8"],
        "displayName": ["wctest8"],
        "gidNumber":["90008"],
        "uidNumber": ["80008"],
        "loginShell": ["/bin/bash"],
        "homeDirectory": ["/home/wctest8"],
        "userPassword" : ["xxxxxxxxx"]
        }

    l.add(gdn,gmodlist)
    l.add(udn,umodlist)

    res = l.search(query="(cn=xx)",basedn="ou=xxxxxx,dc=xxxxxxxx,dc=xxx")
    print(res)
    if len(res) == 1:
            oldmemberUid = res[0][1]["memberUid"]
            oldvalue = {"memberUid":oldmemberUid}
            newmemberUid = oldmemberUid + umodlist["uid"]
            newvalue = {"memberUid":newmemberUid}
            print(oldvalue)
            print(newvalue)
            l.modifying("cn=qa,ou=xxxxxxxxxx,dc=xxxxx,dc=xxx",oldvalue,newvalue)
    else:
        raise "匹配有问题"

