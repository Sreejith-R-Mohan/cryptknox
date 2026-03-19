import secrets, string, random


class Generatepass:    
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
        return "".join(password)

        