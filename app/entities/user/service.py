from sqlalchemy.orm import Session
from app.entities.user.modal import User, UserRoleEnum as UserUserRoleEnum
from app.entities.user.schema import ForgotPassword, UserCreate, UserRead, UserCreateResponse, UserUpdate, UserLogin, UserTokenResponse
from app.core.logging import get_logger
from app.core.email import EmailService
from app.core.security import get_password_hash, generate_random_password, verify_password, create_token
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException
from datetime import datetime, timezone

logger = get_logger(__name__)

# ---------- UserService (single User table, RBAC via user_role) ----------


class UserService:
    """Service for the unified User model (admin + worker in one table)."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.email_service = EmailService()

    def _send_user_email_with_password(self, email: str) -> str:
        """Generate password, hash it, email plain password to user; return hash."""
        random_password = generate_random_password(15)
        hashed = get_password_hash(random_password)
        self.email_service.send_email(
            email,
            "Your Password for WhenWeWork",
            "Your password is: " + random_password,
        )
        return hashed
    
    def check_user_email_exists(self, email: str) -> bool:
        already_exists = self.db.query(User).filter(User.email == email).first()
        return already_exists is not None

    def create_user(
        self,
        payload: UserCreate,
        admin_id: int | None = None,
    ) -> UserCreateResponse:
        """Create a user. Returns user + access_token for immediate use. For workers, pass admin_id."""
        if self.check_user_email_exists(payload.email):
            raise ValueError("User with this email already exists")
        validate_email(payload.email, check_deliverability=False)

        data = payload.model_dump(exclude_unset=True)
        if admin_id is not None:
            data["admin_id"] = admin_id
        if data.get("password"):
            data["password"] = get_password_hash(data["password"])
        else:
            data["password"] = self._send_user_email_with_password(payload.email)
        if data.get("worker_roles") is None:
            data["worker_roles"] = []

        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        role_val = user.user_role.value if hasattr(user.user_role, "value") else str(user.user_role)
        token = create_token({"sub": str(user.id), "role": role_val})
        return UserCreateResponse(
            user=UserRead.model_validate(user),
            access_token=token,
            token_type="Bearer",
        )

    def get_user_by_id(self, user_id: int) -> UserRead | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        return UserRead.model_validate(user) if user else None

    def get_all_workers_by_admin(self, admin_id: int) -> list[UserRead]:
        users = (
            self.db.query(User)
            .filter(User.admin_id == admin_id, User.user_role == UserUserRoleEnum.worker)
            .all()
        )
        return [UserRead.model_validate(u) for u in users] if users else []

    def update_user(self, user_id: int, payload: UserUpdate) -> UserRead | None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        data = payload.model_dump(exclude_unset=True)
        if data.get("password"):
            data["password"] = get_password_hash(data["password"])
        for key, value in data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return UserRead.model_validate(user)

    def delete_user(self, user_id: int) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True

    def login_user(self, payload: UserLogin) -> UserTokenResponse:
        """Login any user (admin or worker); token includes role."""
        try:
            user = self.db.query(User).filter(User.email == payload.email).first()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            if not verify_password(payload.password, user.password):
                raise HTTPException(status_code=401, detail="Invalid password")
            role_val = user.user_role.value if hasattr(user.user_role, "value") else str(user.user_role)
            user_data = {
                "id": user.id,
                "name": f"{user.first_name} {user.last_name}",
                "business_name": user.business.business_name if user.business else None,
                "email": user.email,
                "user_role": user.user_role,
                "last_login_at": datetime.now(timezone.utc),
                "admin_id": user.admin_id,
            }
            admin_id = user.admin_id if user.admin_id else None
            token = create_token({"sub": str(user.id), "role": role_val, "admin_id": admin_id})
            return UserTokenResponse(**user_data, access_token=token, token_type="Bearer")
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error logging in user: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
        
    def reset_password(self, payload: ForgotPassword) -> bool:
        try:
            user = self.db.query(User).filter(User.email == payload.email).first()
            if not user:
                return False
            new_password = self._send_user_email_with_password(payload.email)
            user.password = new_password
            self.db.commit()
            self.db.refresh(user)
            return True
        except Exception as e:
            logger.error(f"Error during forgot password for {payload.email}: {str(e)}")
            raise HTTPException(status_code=500, detail="Unable to reset password at this time.")