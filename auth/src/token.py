# native imports
from datetime import datetime, timedelta, timezone
from pathlib import Path
# extern imports
import jwt

PRIVATE_KEY = Path("/run/secrets/jwt_private").read_text()
PUBLIC_KEY = Path("/run/secrets/jwt_public").read_text()
ALGORITHM = "RS256"
MAX_AGE = 3600 # one hour in seconds

def create_access_token(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "exp": now + timedelta(seconds=MAX_AGE),
    }
    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm=ALGORITHM,
    )

def decode_token(token):
    try:
        _ = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM]
        )
        return "", 200
    except jwt.PyJWTError:
        return "Wrong token", 401