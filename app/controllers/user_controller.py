from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user_model import User
from fastapi.encoders import jsonable_encoder

class UserController:

    def create_user(self, db: Session, user: User):
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return {"resultado": "Usuario creado", "id": user.id}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def get_user(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return jsonable_encoder(user)
        else:
            raise HTTPException(status_code=404, detail="User not found")

    def get_users(self, db: Session):
        users = db.query(User).all()
        if users:
            return {"resultado": jsonable_encoder(users)}
        else:
            raise HTTPException(status_code=404, detail="No users found")

