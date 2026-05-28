from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import smtplib
from email.message import EmailMessage
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

PROJECTS_DB = {
    "dog-breed": {
        "title": "Dog Breed Identification",
        "description": "Deep Learning model using ResNet50 to accurately identify dog breeds from images. Built with TensorFlow and Keras, deployed as a REST API.",
        "hero_image": "/static/assets/dog-breed/dog-1.jpg",
        "images": ["/static/assets/dog-breed/dog-2.jpg", "/static/assets/dog-breed/dog-3.jpg"],
        "github_url": "https://github.com/soumyajitcodes"
    },
    "heart-disease": {
        "title": "Heart Disease Prediction",
        "description": "Machine learning model predicting the likelihood of heart disease based on patient clinical data. Features a streamlined UI for doctors.",
        "hero_image": "/static/assets/heart/heart-1.jpg",
        "images": ["/static/assets/heart/heart-2.jpg", "/static/assets/heart/heart-3.jpg"],
        "github_url": "https://github.com/soumyajitcodes"
    },
    "medical": {
        "title": "Medical Data Analysis",
        "description": "Comprehensive exploratory data analysis pipeline for processing and visualizing large-scale healthcare datasets using Pandas and Seaborn.",
        "hero_image": "/static/assets/medical/medical-1.jpg",
        "images": ["/static/assets/medical/medical-2.jpg", "/static/assets/medical/medical-3.jpg"],
        "github_url": "https://github.com/soumyajitcodes"
    }
}

@app.get("/", response_class=HTMLResponse)
async def my_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/project/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    if project_id not in PROJECTS_DB:
        raise HTTPException(status_code=404, detail="Project not found")
    project = PROJECTS_DB[project_id]
    return templates.TemplateResponse(request=request, name="project_detail.html", context={"project": project})

@app.get("/{page_name}", response_class=HTMLResponse)
async def html_page(request: Request, page_name: str):
    try:
        return templates.TemplateResponse(request=request, name=page_name + ".html")
    except Exception:
        raise HTTPException(status_code=404, detail="Page not found")

def send_email(name, email, subject, message):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    target_email = os.getenv("TARGET_EMAIL", "soumyajitdas.work@outlook.com")

    if not smtp_user or not smtp_password:
        print("SMTP credentials not set. Falling back to CSV.")
        return False

    try:
        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        msg['Subject'] = f"Portfolio Contact: {subject}"
        msg['From'] = smtp_user
        msg['To'] = target_email

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def write_to_csv(name: str, email: str, subject: str, message: str):
    try:
        csv_path = Path(__file__).resolve().parent / 'database.csv'
        with open(csv_path, mode='a', newline='', encoding='utf-8') as database:
            csv_writer = csv.writer(database, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([name, email, subject, message])
    except Exception as e:
        print(f"Warning: Could not write to CSV (read-only filesystem?): {e}")

@app.post("/submit_form")
def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    email_sent = send_email(name, email, subject, message)
    if not email_sent:
        write_to_csv(name, email, subject, message)
    
    return RedirectResponse(url="/thankyou", status_code=303)

if __name__ == '__main__':
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
