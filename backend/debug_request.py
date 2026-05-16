import urllib.request

try:
    response = urllib.request.urlopen('http://127.0.0.1:8002/')
    print('status', response.status)
    print(response.read(200).decode('utf-8', errors='ignore'))
except Exception as e:
    import traceback
    traceback.print_exc()
