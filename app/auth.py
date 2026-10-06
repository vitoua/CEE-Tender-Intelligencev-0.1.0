from passlib.context import CryptContext
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto')
def hash_password(v):return pwd.hash(v)
def verify_password(v,h):return pwd.verify(v,h)
