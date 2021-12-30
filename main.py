from wsgiref.simple_server import make_server
from server.app import build_app

if __name__ == '__main__':
    app = build_app()
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()

