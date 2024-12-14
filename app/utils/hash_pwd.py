from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password, hashed_password):
    print(plain_password, hashed_password)
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password):
    return PWD_CONTEXT.hash(password)
