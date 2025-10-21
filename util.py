import base64
import env_secrets

def _repeat_bytes(key: bytes, length: int) -> bytes:
    return (key * (length // len(key) + 1))[:length]

def decrypt(password: str) -> str:
    encrypted = base64.b64decode(env_secrets.ENCRYPTED_OPENAI_API_KEY.encode('ascii'))
    key = password.encode('utf-8')
    plain = bytes(a ^ b for a, b in zip(encrypted, _repeat_bytes(key, len(encrypted))))
    return plain.decode('utf-8')