#!/usr/bin/env python3
"""Start a static server on the first free port at/above --start."""
from pathlib import Path
import argparse, http.server, socket, socketserver
ROOT=Path(__file__).resolve().parents[1]
def is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex(('127.0.0.1', port)) != 0
parser=argparse.ArgumentParser(); parser.add_argument('--start', type=int, default=8790); parser.add_argument('--max', type=int, default=8899)
args=parser.parse_args(); port=next((p for p in range(args.start,args.max+1) if is_free(p)), None)
if port is None: raise SystemExit(f'No free port found from {args.start} to {args.max}')
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT),**kw)
with socketserver.TCPServer(('127.0.0.1', port), Handler) as httpd:
    print(f'Stratos Command Center running at http://localhost:{port}', flush=True)
    httpd.serve_forever()
