import sqlalchemy as _alc
from sqlalchemy import orm as _alc_orm
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///sports_events.db"
Base = _alc_orm.declarative_base()


class BaseDB(Base):
    __abstract__ = True

    def save(self, db: _alc_orm.Session):
        """Save the instance to the database."""
        db.add(self)
        db.commit()
        db.refresh(self)
        return self

    @classmethod
    def delete_all(cls, db: _alc_orm.Session):
        """Delete all instances of the model from the database."""
        db.query(cls).delete()
        db.commit()

    @classmethod
    def get_all(cls, db: _alc_orm.Session):
        """Gets all instances of the model from the database."""
        return db.query(cls).all()


engine = _alc.create_engine(DATABASE_URL, echo=False)
SessionLocal = _alc_orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
