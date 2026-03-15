import json
class Items:
    

    def create_new_entry(self):
        return {
            "entries":{}
        }


    def add_or_update_entry(self, vault, service, uname, passwd):
        vault["entries"].setdefault(service,{})

        acc = vault["entries"][service]

        # if acc already exist in vault, ask the user, to update/cancel else insert

        if uname in acc:
            choice = input(
                f"Account {uname} already exists for {service}. Update password? (y/n)"
            )

            if choice.lower == 'y':
                acc[uname] = passwd
                print(f"Password Updated for {uname}")
            else:
                print("Operation Cancelled...")
        else:
            acc[uname] = passwd
            print("New account added")

        return vault
    
    def delete_entry(self, vault, service, uname):

        entries = vault.get("entries", {})

        if service.lower() == "all":

            confirm = input("Delete ALL entries? (y/n): ")

            if confirm.lower() == "y":
                entries.clear()
                print("All entries deleted.")
            else:
                print("Operation cancelled.")

            return vault

        # delete specific account
        if service not in entries:
            print("Service not found")
            return vault

        if uname not in entries[service]:
            print("Username not found")
            return vault

        del entries[service][uname]

        print(f"{uname} deleted successfully")

        # remove service if empty
        if not entries[service]:
            del entries[service]

        return vault
    
    def show_entries(self, vault, service="all"):
        entries = vault.get("entries",{})

        if service.lower == 'all':
            if not entries:
                print("Vault is empty...")
                return
            
            for sname, account in entries.items():
                print(f"\nService {sname}")
                for uname, passwd in account.items():
                    print(f"\nUsername : {uname} | Password : {passwd}")

        else:
            accounts = entries.get(service)

            if not accounts:
                print("Service not found.")
                return
            
            print(f"Service:{service}")
            for uname, passwd in account.items():
                    print(f"\nUsername : {uname} | Password : {passwd}")

