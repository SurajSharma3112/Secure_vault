from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import user_auth
import database
import encrypter
import os
import shutil

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="super_secret_fastapi_key_for_vault")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
def startup_event():
    database.setup_database()

@app.get("/", response_class=HTMLResponse)

async def index(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    success, result = user_auth.login_user(username, password)
    if success:
        request.session["user_id"] = result
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "error": result})

@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"request": request, "error": None})

@app.post("/register", response_class=HTMLResponse)
async def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
    success, message = user_auth.register_user(username, password)
    if success:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request=request, name="register.html", context={"request": request, "error": message})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)
        
    connection = database.get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM file_metadata WHERE user_id = %s ORDER BY upload_timestamp DESC", (user_id,))
    files = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"request": request, "files": files})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    encrypted_filepath = encrypter.encrypt_file(filepath)
    encrypted_filename = os.path.basename(encrypted_filepath)
    file_size = os.path.getsize(encrypted_filepath)

    connection = database.get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO file_metadata (user_id, original_filename, encrypted_filename, file_size) VALUES (%s, %s, %s, %s)",
        (user_id, file.filename, encrypted_filename, file_size)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/download/{file_id}")
async def download_file(request: Request, file_id: int):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    connection = database.get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM file_metadata WHERE id = %s AND user_id = %s", (file_id, user_id))
    file_data = cursor.fetchone()
    cursor.close()
    connection.close()

    if not file_data:
        return RedirectResponse(url="/dashboard", status_code=303)

    encrypted_filepath = os.path.join(UPLOAD_DIR, file_data['encrypted_filename'])
    if not os.path.exists(encrypted_filepath):
        return RedirectResponse(url="/dashboard", status_code=303)

    decrypted_filepath = encrypter.decrypt_file(encrypted_filepath)
    
    return FileResponse(decrypted_filepath, filename=file_data['original_filename'])

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse(url="/login", status_code=303)
