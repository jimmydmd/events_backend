from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request


from events_app_backend.events.routes import router as events_router
from events_app_backend.registrations.routes import router as registrations_router
from events_app_backend.auth.routes_auth import router as auth_router
from events_app_backend.users.routes import router as users_router
from events_app_backend.roles.routes import router as roles_router



app = FastAPI()

origins = [
    "http://localhost:3000",  # React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events_router, prefix="/events", tags=["Events"])
app.include_router(registrations_router, prefix="/registrations", tags=["Registrations"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(roles_router, prefix="/roles", tags=["Roles"])

app.include_router(auth_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []

    for err in exc.errors():
        loc = err.get("loc", [])
        if loc and loc[0] == "body":
            field = ".".join(str(l) for l in loc[1:])
        else:
            field = ".".join(str(l) for l in loc)

        formatted_errors.append({
            "field": field,
            "message": err.get("msg")
        })

    return JSONResponse(
        status_code=422,
        content={"detail": formatted_errors}
    )


