import json
class Items:
    

    def create_new_entry(self):
        return {
            "entries":{}
        }

    def add_new_entry(self, vault, service, uname, passwd):
        vault["entries"][service] = {
            "username": uname,
            "password": passwd
        }
        return vault
