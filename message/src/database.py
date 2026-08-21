import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError, StatementError

from src.tables import Base

engine = create_engine(os.environ.get("POSTGRES_URL"))

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base.metadata.create_all(bind=engine)

def get_db():
    db : Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_to_db(db: Session, obj):
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return "", 200
    except IntegrityError as e:
        db.rollback()
        return f"Integrity error : {e}", 403
    except DataError as e:
        db.rollback()
        return f"Invalid data : {e}", 403
    except StatementError as e:
        db.rollback()
        return f"Request error : {e}", 403
    except SQLAlchemyError as e:
        db.rollback()
        return f"Database error : {e}", 403
    except Exception as e:
        db.rollback()
        return f"Unknown error : {e}", 403

def delete_in_db(db: Session, obj):
    try:
        db.delete(obj)
        db.commit()
        return "", 200
    except Exception as e:
        db.rollback()
        return f"Unknown error : {e}", 403
