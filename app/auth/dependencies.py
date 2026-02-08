from fastapi import Request, HTTPException, status

def require_login(request: Request):
    if not request.session.get("user"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )