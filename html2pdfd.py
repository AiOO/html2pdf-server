#!/usr/bin/env python3
import argparse
import io
import json

from waitress import serve
from weasyprint import HTML
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

__all__ = 'app',


SUPPORTED_TYPES = {
    'application/pdf': lambda html, buffer: html.write_pdf(buffer)
}

MAX_HTML_SIZE = 1024 * 1024 * 50  # 50MiB


@Request.application
def app(request: Request):
    if request.path != '/':
        return Response(
            json.dumps({
                'error': 'not-found',
                'message': "page not found; there's only one path: /"
            }),
            status=404
        )
    elif request.method.upper() != 'POST':
        return Response(
            json.dumps({
                'error': 'method-not-allowed',
                'message': 'only POST method is allowed'
            }),
            status=405
        )
    elif request.mimetype not in {'text/html', 'application/xhtml+xml'}:
        return Response(
            json.dumps({
                'error': 'bad-request',
                'message': 'content has to be HTML'
            }),
            status=400
        )
    matched = request.accept_mimetypes.best_match(SUPPORTED_TYPES.keys())
    if not matched:
        return Response(
            json.dumps({
                'error': 'not-acceptable',
                'message': 'unsupported type; the list of supported '
                           'types: ' + ', '.join(SUPPORTED_TYPES)
            }),
            status=406
        )
    html = HTML(string=request.get_data(as_text=True))
    pdf_buffer = io.BytesIO()
    SUPPORTED_TYPES[matched](html, pdf_buffer)
    pdf_buffer.seek(0)
    return Response(pdf_buffer, mimetype=matched)


def main():
    parser = argparse.ArgumentParser(
        description='HTTP server that renders HTML to PDF'
    )
    parser.add_argument('--host', '-H',
                        default='0.0.0.0', help='host to listen [%default]')
    parser.add_argument('--port', '-p',
                        type=int, default=8080,
                        help='port to listen [%default]')
    parser.add_argument('--debug', '-d',
                        action='store_true', help='debug mode')
    args = parser.parse_args()
    if args.debug:
        run_simple(args.host, args.port, app,
                   use_debugger=True, use_reloader=True)
    else:
        serve(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
