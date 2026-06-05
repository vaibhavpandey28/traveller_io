from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
import os
from app.core.logger import get_logger
from app.api import auth as auth_v1
from app.helpers.exceptionHandler import setup_exception_handlers
from app.middleware.token_middleware import add_token_middleware

load_dotenv() 

logger = get_logger(__name__)
app = FastAPI()


# Set up custom exception handlers
setup_exception_handlers(app)

# Add token middleware (requires `token` header on every request)
add_token_middleware(app)

# Register API routers
app.include_router(auth_v1.router, prefix="/api/v1")


def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema

	openapi_schema = get_openapi(
		title=app.title,
		version=app.version,
		description=app.description,
		routes=app.routes,
	)

	# Add Bearer auth scheme so the Swagger UI shows the Authorize button
	openapi_schema.setdefault("components", {})
	openapi_schema["components"].setdefault("securitySchemes", {})
	openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
		"type": "http",
		"scheme": "bearer",
		"bearerFormat": "JWT",
	}

	# Apply globally so protected routes can use it (UI will show Authorize)
	openapi_schema.setdefault("security", [{"BearerAuth": []}])

	app.openapi_schema = openapi_schema
	return app.openapi_schema


app.openapi = custom_openapi

