import os
from platformdirs import user_data_dir

class Storage:
    def __init__(self):
        self.APP_NAME = "cryptknox"
        self.FILE_PATH = os.path.join(user_data_dir(self.APP_NAME),".vault.enc")

    def save_file(self, data):
        os.makedirs(os.path.dirname(self.FILE_PATH),exist_ok=True)
        with open(self.FILE_PATH,'wb') as f:
            f.write(data)


    def load_file(self):

        if not os.path.exists(self.FILE_PATH):
            return None
        
        with open(self.FILE_PATH,'rb') as f:
            return f.read()