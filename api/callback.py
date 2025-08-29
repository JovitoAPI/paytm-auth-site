# api/callback.py
# A tiny Vercel Python function that reads the query string and shows whatever
# Paytm Money sends back (code/request_token, state, error, etc.)

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Paytm Money Callback</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; padding: 24px; max-width: 800px; margin: auto; }
    code, pre { background:#f6f8fa; padding: 8px 12px; border-radius: 6px; display:block; }
    .ok { color: #0a7f3f; font-weight: 700; }
    .warn { color: #b26b00; font-weight: 700; }
    .err { color: #c1121f; font-weight: 700; }
    table { border-collapse: collapse; margin-top: 12px; }
    td, th { border: 1px solid #ddd; padding: 8px 10px; }
    th { background: #fafafa; text-align: left; }
  </style>
</head>
<body>
  <h2>Paytm Money Authentication Callback</h2>
  {body}
  <h3>Raw query parameters</h3>
  <pre>{raw}</pre>
</body>
</html>
"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query or "")
        # Flatten single values
        flat = {k: (v[0] if isinstance(v, list) and v else v) for k, v in params.items()}

        # Decide what to show
        section = []
        if "code" in flat:
            section.append(f"<p class='ok'>✅ Authorization code received:</p><code>{flat['code']}</code>")
        elif "request_token" in flat:
            section.append(f"<p class='ok'>✅ Request token received:</p><code>{flat['request_token']}</code>")
        elif "error" in flat:
            section.append(f"<p class='err'>❌ Error:</p><code>{flat.get('error_description', flat['error'])}</code>")
        else:
            section.append("<p class='warn'>⚠️ No <code>code</code> or <code>request_token</code> found in the URL.</p>")
            section.append("<p>This page still works — it shows whatever the provider returned so we can diagnose.</p>")

        # Optional: Show state if present
        if "state" in flat:
            section.append(f"<p>State:</p><code>{flat['state']}</code>")

        body = "\n".join(section)
        html = HTML.format(body=body, raw=json.dumps(flat, indent=2))

        # Reply
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))
