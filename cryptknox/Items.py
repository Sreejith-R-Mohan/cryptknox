from tabulate import tabulate


class Items:
    

    def create_new_entry(self):
        return {
            "entries":{}
        }
    
    @staticmethod
    def print_table(rows):
        print(tabulate(rows, headers=["Service", "Username", "Password"], tablefmt="pretty"))

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
    
    def delete_entry(self, vault, uname, service):

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
        if uname:
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
        else:
            if service not in entries:
                print("Service not found")
                return vault
            acc = entries.get(service)
            length = len(acc)
            
            if length>0:
                choice = input(f"Found {length} entries under {service}.\n Do you want to wipe them al(y/n) ?")
                if choice.lower() == "y":
                    del entries[service]
                    print(f"All entries deleted under {service}")
                else:
                    print("Operation cancelled.")

            return vault
    
    def show_entries(self, vault, uname, service="all"):
        entries = vault.get("entries",{})
        rows = []
        if service.lower() == 'all':
            if not entries:
                print("Vault is empty...")
                return
            
            for sname, account in entries.items():
                for uname, passwd in account.items():
                    rows.append([sname, uname, passwd])
        elif uname:
            accounts = entries.get(service)

            if not accounts:
                print("Service not found.")
                return

            passwd = accounts.get(uname)

            if not passwd:
                print("Username not found.")
                return

            rows.append([service, uname, passwd])
        else:
            # print(entries)

            accounts = entries.get(service)

            if not accounts:
                print("Service not found.")
                return
            
            for uname, passwd in accounts.items():
                    rows.append([service, uname, passwd])
        
        self.print_table(rows)

