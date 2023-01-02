import hashlib
import sys

contraseña = sys.argv[1]
hash = hashlib.sha256(contraseña.encode()).hexdigest()
print(hash)