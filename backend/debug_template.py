import os
from starlette.templating import Jinja2Templates

print('cwd=', os.getcwd())
print('exists=', os.path.exists('front/templates/index.html'))

try:
    templates = Jinja2Templates(directory='front/templates')
    print('loader=', templates.env.loader)
    template = templates.get_template('index.html')
    print('template loaded', template)
except Exception as e:
    import traceback
    traceback.print_exc()
