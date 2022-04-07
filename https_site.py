from http.server import HTTPServer,SimpleHTTPRequestHandler
from socketserver import BaseServer
import ssl

httpd = HTTPServer(('0.0.0.0', 8443), SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, server_side=True, keyfile="site_home_local.key", certfile="site_home_local.crt", ca_certs="data/step-ca/certs/root_ca.crt")
httpd.serve_forever()
