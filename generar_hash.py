import bcrypt

def generar_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

print("adminpass:", generar_hash("adminpass"))
print("normalpass:", generar_hash("normalpass"))
