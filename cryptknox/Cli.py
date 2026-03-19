# ! /usr/bin/python
from .lib.Arguments import Arguments
from .algorithm.Aes import Aes
from .algorithm.Generatepass import Generatepass
import sys,json
from .Items import Items
from .Storage import Storage
from . import __version__

class Cli:


    allowed_options = ('--operation','-o','--master-password','-m','--service','-s','--username','-u','--password','-p','--length','-l','--help','-h','--version','-v')
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

    Optional Options:
        --username, -u            Retrieve a specific username under a service

    Behavior:
        - If --service all → retrieves all entries
        - If --service <service> → retrieves all usernames under that service
        - If --service <service> + --username <username> → retrieves only that account

    Examples:
        cryptknox -o retrieve -m MySecretPassword -s gmail
        cryptknox -o retrieve -m MySecretPassword -s gmail -u user@gmail.com
        cryptknox -o retrieve -m MySecretPassword -s all


delete
    Delete stored credentials from the vault.

    Required Options:
        --master-password, -m     Master password used to decrypt the vault
        --service, -s             Service name or "all"

    Optional Options:
        --username, -u            Delete a specific username under a service

    Behavior:
        - If --service all → deletes all entries (confirmation required)
        - If --service <service> → deletes all usernames under that service
        - If --service <service> + --username <username> → deletes only that account

    Examples:
        cryptknox -o delete -m MySecretPassword -s gmail
        cryptknox -o delete -m MySecretPassword -s gmail -u user@gmail.com
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
--version, -v            Show the installed version of CryptKnox


EXAMPLES

Show version
    cryptknox --version

Store credentials
    cryptknox -o store -m MySecretPassword -s gmail -u user@gmail.com -p mypassword

Retrieve all credentials
    cryptknox -o retrieve -m MySecretPassword -s all

Retrieve specific account
    cryptknox -o retrieve -m MySecretPassword -s gmail -u user@gmail.com

Generate a password
    cryptknox -o generate -l 16

Delete all credentials under a service
    cryptknox -o delete -m MySecretPassword -s gmail

Delete specific account
    cryptknox -o delete -m MySecretPassword -s gmail -u user@gmail.com

Delete entire vault
    cryptknox -o delete -m MySecretPassword -s all
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
                except Exception as e:
                    print("Cannot able to decrypt the vault: Check master key")
            else:
                dec_con = items.create_new_entry()
            
             # call add_new_entry in the vault
            data = items.add_or_update_entry(dec_con,service,uname,passwd)

            encrypted = aes.encrypt(json.dumps(data).encode())

            storage.save_file(encrypted)

        elif operation == 'retrieve':
            master_passwd = self._get_required('--master-password','-m','Master Operation')
            service = self._get_required('--service','-s','Service')

            uname = None
            if self.args.hasOption('-u') or self.args.hasOption('--username'):
                uname = self.args.getOptionValue('--username') or self.args.getOptionValue('-u')
            

            # get the file
            data = storage.load_file()
            
            # decrypt it
            aes = Aes(master_passwd)
            dec_con = aes.decrypt(data).decode()
            # dump json
            json_data = json.loads(dec_con)
            # read it from the json using service Name

            # will call the function which will display the service in a formatted way

            items.show_entries(json_data,uname,service) # check this

        elif operation == 'generate':
            length = self._get_required('--length','-l','Length')

            genpass = Generatepass()
            password = genpass.generate_pass(length)
            print(f"Generated password : {password}")


        elif operation == 'delete':
            master_passwd = self._get_required('--master-password','-m','Master Operation')
            service = self._get_required('--service','-s','Service')
            uname = None
            if self.args.hasOption('-u') or self.args.hasOption('--username'):
                uname = self.args.getOptionValue('--username') or self.args.getOptionValue('-u')
            # get the file
            data = storage.load_file()
            
            # decrypt it
            aes = Aes(master_passwd)
            dec_con = aes.decrypt(data).decode()
            # print(dec_con)


            # dump json
            json_data = json.loads(dec_con)
            new_json = items.delete_entry(json_data,uname,service)
            # print(new_json)


            file_data = storage.load_file()

            new_enc = aes.encrypt(json.dumps(new_json).encode())

            storage.save_file(new_enc)

    
        

def main():
    try:
        args = sys.argv[1:]
        # print(sys.argv)
        if not args:
            Cli.help()
            sys.exit(0)

        if "--help" in args or "-h" in args:
            Cli.help()
            sys.exit(0)

        if "--version" in args or "-v" in args:
            print(f"cryptknox {__version__}")
            sys.exit(0)

        Cli(sys.argv).run()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()