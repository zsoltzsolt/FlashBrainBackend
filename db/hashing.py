from passlib.context import CryptContext

password_context = CryptContext(schemes='bcrypt', deprecated='auto')

class Hash:
    def hash_password(password: str):
        return password_context.hash(password)

    def verify(hashed_password: str, plain_password: str):
        return password_context.verify(plain_password, hashed_password)