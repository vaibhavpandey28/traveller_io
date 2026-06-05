from fastapi import Request
from starlette.responses import JSONResponse
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM


def add_token_middleware(app):

    # Exempt paths: we want to allow unauthenticated access to the
    # auth endpoints (which are mounted under /api/v1/auth) and to docs.
    EXEMPT_PATH_PREFIXES = ("/docs", "/redoc", "/openapi.json")
    EXEMPT_PATH_SUFFIXES = ("/login", "/register")

    @app.middleware("http")
    async def check_token(request: Request, call_next):

        # Allow OPTIONS preflight without token
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path

        # If the request is for docs or openapi, allow through
        if any(path.startswith(p) for p in EXEMPT_PATH_PREFIXES):
            return await call_next(request)

        # If the request ends with /login or /register (e.g. /api/v1/auth/login), allow through
        if any(path.endswith(s) for s in EXEMPT_PATH_SUFFIXES):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                {"detail": "Authorization header missing"},
                status_code=401
            )

        try:
            scheme, token = auth_header.split()

            if scheme.lower() != "bearer":
                return JSONResponse(
                    {"detail": "Invalid authentication scheme"},
                    status_code=401
                )

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            request.state.token_data = payload

        except ValueError:
            return JSONResponse(
                {"detail": "Invalid Authorization header format"},
                status_code=401
            )

        except JWTError:
            return JSONResponse(
                {"detail": "Invalid or expired token"},
                status_code=401
            )

        return await call_next(request)