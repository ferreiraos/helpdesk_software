from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.testclient import TestClient

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = str(BASE_DIR / "front" / "templates")

templates = Jinja2Templates(directory=TEMPLATE_DIR)
print('template dir', TEMPLATE_DIR)
print('created', templates)
print('loader', templates.env.loader)
try:
    tpl = templates.get_template('index.html')
    print('template loaded', tpl)
except Exception:
    import traceback
    traceback.print_exc()

app = FastAPI()

@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, 'chamados': []})

client = TestClient(app)
try:
    response = client.get('/')
    print('status', response.status_code)
    print(response.text[:200])
except Exception:
    import traceback
    traceback.print_exc()
