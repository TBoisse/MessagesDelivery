# native imports
import os
import logging
logger = logging.getLogger(__name__)
from datetime import timedelta
# extern imports
from fastapi import FastAPI, HTTPException, Request
from fastapi.security import HTTPBearer
from hashids import Hashids
from minio import Minio, error
# fast api
app = FastAPI()
security = HTTPBearer()
# hash func
hashids = Hashids(
    salt=os.environ.get("USERS_KEY"),
    min_length=14,
)
# minio
minio_client = Minio(
    "http://minio:9000",
    access_key=os.environ.get("MINIO_USER"),
    secret_key=os.environ.get("MINIO_PWD"),
    secure=False,
)
USERS_BUCKET = "users"
BASE_MINIO_URL = os.environ.get("BASE_MINIO_URL")

def get_object_name(object_type : str, user_id : str, object_name : str):
    return f"{object_type}/{user_id}/{object_name}"

@app.get("/me/icon")
def get_icon(request : Request):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    try:
        object_name = get_object_name("icons", hashids.encode(user_id), "icons.png")
        minio_client.stat_object(
            bucket_name=USERS_BUCKET,
            object_name=object_name,
        )
        return {"url" : f"{BASE_MINIO_URL}/{USERS_BUCKET}/{object_name}"}
    except error.S3Error as e:
        if e.code in ("NoSuchKey", "NoSuchObject", "NoSuchBucket"):
            return {"url" : ""}
        raise e

@app.put("/me/icon")
def put_icon(request : Request):
    try:
        user_id = int(request.headers.get("X-User-Id"))
    except Exception:
        raise HTTPException(status_code=401)
    object_name = get_object_name("icons", hashids.encode(user_id), "icons.png")
    presigned_url = minio_client.presigned_put_object(
        bucket_name=USERS_BUCKET,
        object_name=object_name,
        expires=timedelta(minutes=1),
    )
    return {"url" : presigned_url}