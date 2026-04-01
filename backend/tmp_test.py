from app.core.security import get_password_hash

try:
    get_password_hash('x'*100)
except Exception as e:
    print('err', type(e).__name__, e)
print('ok')
