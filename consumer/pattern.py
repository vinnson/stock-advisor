import requests
import json
import os
from pygments import highlight, lexers, formatters

r = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol=GEVO&resolution=D&token='+ os.environ.get('FINNHUB_TOKEN'))


parsed = json.loads(r.content.decode("utf-8"))
formatted = json.dumps(parsed, indent=2, sort_keys=True)

colorful_json = highlight(formatted, lexers.JsonLexer(), formatters.TerminalFormatter())
print(colorful_json)
