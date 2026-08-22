from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.user import User


def require_role(required_role: str):
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        user_roles = {
            role.name.upper()
            for role in current_user.roles
        }

        if required_role.upper() not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )

        return current_user

    return role_checker


require_admin = require_role("ADMIN")
require_scheduler = require_role("SCHEDULER")
require_instructor = require_role("INSTRUCTOR")
require_student = require_role("STUDENT")