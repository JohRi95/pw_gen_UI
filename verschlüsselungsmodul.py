import base64
import ast
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PW_DICTIONARY = "password_dict.json"

def derive_key(pass_from_user):

    """Leitet in mehreren Schritten einen Key aus einem Userpasswort ab:
    1. Fragt den User nach einen Input = pass_from_user
    2. Wandelt string nach utf-8 in bytes um
    3. Über Funktion salt_from_password wird ein Saltvariable aus dem Userpasswort generiert
    4. Die Saltvariable aus salt_from_password() als salt verwendet, um den file_key aus salt + passwort abzuleiten"""

    def salt_from_password(password):

        salt = password

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        salt = base64.urlsafe_b64encode(kdf.derive(password))

        return salt

#    pass_from_user = input("Provide a Password: ")
    password = pass_from_user.encode()

    my_salt = salt_from_password(password)

    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = my_salt,
        iterations = 100000,
        backend=default_backend()
    )

    return base64.urlsafe_b64encode(kdf.derive(password))

def encode_file(pass_from_user):

    """ Funktion leitet key ab, liest file ein und verschlüsselt ihn mit key aus derive_key Funktion"""

    cipher = Fernet(derive_key(pass_from_user))

    with open(PW_DICTIONARY, "rb") as file:
        data = file.read()

    with open(PW_DICTIONARY, "wb") as file:
        file.write(cipher.encrypt(data))

def write_encoded_data(pass_from_user):

    cipher = Fernet(derive_key(pass_from_user))

    with open(PW_DICTIONARY, "wb") as file:
        file.write(cipher.encrypt(byte_data))

def validate_password(pass_from_user):

    """ Funktion validiert passwort. Bei positiver Validierung, wird .json entschlüsselt
    1. Fernet Objekt wird aus Funktion erstellt und als cipher gespeichert.
    2. Es wird die .json geöffnet, bzw. ausgelesen
    3.1 try: wenn data aus file decrypted werden kann, dann ist das eingegeben passwort korrekt, da der
    abgeleitete key mit dem key der Verschlüsselung übereinstimmt. Es wird dann die Funktion write_decoded_file aufgerufen
    3.1.1 write_decoded_file öffnet nun die Datei und entschlüsselt sie.
    3.2 except: falls 3.1 nicht eintritt, ist das eingegebene passwort falsch, da die keys nicht übereinstimmen."""

    cipher = Fernet(derive_key(pass_from_user))

    with open(PW_DICTIONARY, "rb") as file:
        data = file.read()
        try:
            if cipher.decrypt(data):
#                write_decoded_file()
                decoded_data = cipher.decrypt(data)
                decoded_data = ast.literal_eval(decoded_data.decode('utf-8'))
                return True, decoded_data
        except:
           return False, None
