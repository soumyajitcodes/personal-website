from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def my_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/{page_name}", response_class=HTMLResponse)
async def html_page(request: Request, page_name: str):
    # This acts as a catch-all for HTML pages
    return templates.TemplateResponse(request=request, name=page_name)

def write_to_csv(name: str, email: str, subject: str, message: str):
    # Writing to CSV synchronously, FastAPI will run this in a threadpool
    with open('database.csv', mode='a', newline='', encoding='utf-8') as database:
        csv_writer = csv.writer(database, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, subject, message])

@app.post("/submit_form")
def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...)
):
    write_to_csv(name, email, subject, message)
    # Redirecting to thankyou.html after submission
    return RedirectResponse(url="/thankyou.html", status_code=303)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=5000, reload=True)
