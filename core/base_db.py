from sqlalchemy import orm as _alc_orm

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
