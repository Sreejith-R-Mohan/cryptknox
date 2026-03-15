#! /usr/bin/python
from .lib.Arguments import Arguments
from .algorithm.Aes import Aes
import sys,json
from .Items import Items
from .Storage import Storage

import secrets, string, random
class Cli:


    allowed_options = ('--operation','-o','--master-password','-m','--service','-s','--username','-u','--password','-p','--length','-l','--help','-h')
    @staticmethod
    def help():
        HELP_TEXT = """
CryptKnox – Encrypted CLI Password Manager

USAGE
    cryptknox --operation|-o [store|retrieve|delete|generate] [OPTIONS]

OPERATIONS

    store
        Store a new password entry in the encrypted vault.

        Required Options:
            --master-password, -m     Master password used to encrypt/decrypt the vault
            --service, -s             Service name (example: gmail)
            --username, -u            Username for the service
            --password, -p            Password to store

        Example:
            cryptknox -o store -m MySecretPassword -s gmail -u user@gmail.com -p mypassword


    retrieve
        Retrieve stored credentials from the vault.

        Required Options:
            --master-password, -m     Master password used to decrypt the vault
            --service, -s             Service name or "all"

        Example:
            cryptknox -o retrieve -m MySecretPassword -s gmail
            cryptknox -o retrieve -m MySecretPassword -s all


    delete
        Delete stored credentials from the vault.

        Required Options:
            --master-password, -m     Master password used to decrypt the vault
            --service, -s             Service name or "all"

        Example:
            cryptknox -o delete -m MySecretPassword -s gmail
            cryptknox -o delete -m MySecretPassword -s all


    generate
        Generate a secure random password.

        Required Options:
            --length, -l              Length of password (must be greater than 4)

        Example:
            cryptknox -o generate -l 12


OPTIONS

    --operation, -o          Operation to perform
    --master-password, -m    Master password for vault encryption
    --service, -s            Service name (example: gmail) or "all"
    --username, -u           Username associated with the service
    --password, -p           Password to store
    --length, -l             Length of generated password
    --help, -h               Show this help message


EXAMPLES

    Store credentials
        cryptknox -o store -m MySecretPassword -s gmail -u user@gmail.com -p mypassword

    Retrieve all credentials
        cryptknox -o retrieve -m MySecretPassword -s all

    Generate a password
        cryptknox -o generate -l 16

    Delete credentials
        cryptknox -o delete -m MySecretPassword -s gmail
"""
        print(HELP_TEXT)

    def __init__(self,args):
        self.args = Arguments(args)


    def _get_required(self, long_opt, short_opt, name):
        """Helper function to fetch CLI option values"""

        args = self.args

        if not(args.hasOption(long_opt) or args.hasOption(short_opt)):
            raise ValueError(f"Enter {name}")
        
        val = args.getOptionValue(long_opt) or args.getOptionValue(short_opt)

        if not val:
            raise ValueError(f"Enter {name} value")
        return val
    

    def run(self):
        args = self.args

        # if has option other than allowed options raise Exception

        for i in args.options:
            if i not in self.allowed_options:
                self.help()
                raise ValueError("Unknown arguments...")

        # Get operation value
        operation = self._get_required('--operation','-o','Operation')
        

        storage = Storage() 
        items = Items()

        if operation == 'store':   
            master_passwd = self._get_required('--master-password','-m','Master Operation')
            service = self._get_required('--service','-s','Service')
            uname = self._get_required('--username','-u',"Username")
            passwd = self._get_required('--password','-p','Password')

            # check if vault exists, if not load one else decrypt the vault.
                      
            file_data = storage.load_file()


            aes = Aes(master_passwd)
            if file_data:
                try:
                    decrypt_vault = aes.decrypt(file_data)
                    dec_con = json.loads(decrypt_vault)
                except ValueError as e:
                    print("Cannot able to decrypt the vault: Check master key", e)
            else:
                dec_con = items.create_new_entry()
            
             # call add_new_entry in the vault
            data = items.add_or_update_entry(dec_con,service,uname,passwd)

            encrypted = aes.encrypt(json.dumps(data).encode())

            storage.save_file(encrypted)

        elif operation == 'retrieve':
            master_passwd = self._get_required('--master-password','-m','Master Operation')
            service = self._get_required('--service','-s','Service')
            

            # get the file
            data = storage.load_file()
            
            # decrypt it
            aes = Aes(master_passwd)
            dec_con = aes.decrypt(data).decode()
            # dump json
            json_data = json.loads(dec_con)
            # read it from the json using service Name

            # will call the function which will display the service in a formatted way

            items.show_entries(json_data, service)

        elif operation == 'generate':
            length = self._get_required('--length','-l','Length')
            self.generate_pass(length)

        elif operation == 'delete':
            master_passwd = self._get_required('--master-password','-m','Master Operation')
            service = self._get_required('--service','-s','Service')
            uname = self._get_required('--username','-u','Username')
            # get the file
            data = storage.load_file()
            
            # decrypt it
            aes = Aes(master_passwd)
            dec_con = aes.decrypt(data).decode()
            print(dec_con)
            # dump json
            json_data = json.loads(dec_con)
            items.delete_entry(json_data,service,uname)
            
        

    def generate_pass(self, length):
        # Since it is coming as a string from the command line
        length = int(length)
        if length < 4:
            raise ValueError("Length must be greater than 4")
        
        # This will ensure the password will contain 1 lowercase, 1 uppercase , 1 digit, 1 special character
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(string.punctuation)
        ]

        all_char = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

        for i in range(length - 4):
            password.append(secrets.choice(all_char))
        
        random.shuffle(password)
        # Convert array to string
        password = "".join(password)

        print(password)
        

def main():
    try:
        if len(sys.argv)==1 or "--help" in sys.argv or "-h" in sys.argv:
            Cli.help()
            sys.exit(1)
        if len(sys.argv) <= 2:
            print("Oops:< Missing required arguments\n")
            Cli.help()
            sys.exit(1)   

        Cli(sys.argv).run()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()