from flask import Flask, request, jsonify
import json

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>txt2json</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; font-family: monospace; background: #111; color: #ddd; }
  header { padding: 12px 16px; border-bottom: 1px solid #333; font-size: 14px; }
  .wrap { display: flex; height: calc(100vh - 45px); }
  .col { flex: 1; display: flex; flex-direction: column; padding: 16px; }
  .col + .col { border-left: 1px solid #333; }
  label { font-size: 12px; color: #888; margin-bottom: 8px; }
  textarea { flex: 1; resize: none; background: #1a1a1a; color: #ddd;
    border: 1px solid #333; padding: 12px; font: inherit; outline: none; }
  textarea:focus { border-color: #555; }
</style>
</head>
<body>
<header>txt2json &mdash; one "key: value" per line</header>
<div class="wrap">
  <div class="col">
    <label>text</label>
    <textarea id="in" placeholder="example:&#10;name: John Doe&#10;age: 25&#10;email: john@doe.com"></textarea>
  </div>
  <div class="col">
    <label>json (body)</label>
    <textarea id="out" readonly placeholder="{}"></textarea>
  </div>
</div>
<script>
const inp = document.getElementById('in');
const out = document.getElementById('out');
let t;
inp.addEventListener('input', () => {
  clearTimeout(t);
  t = setTimeout(async () => {
    const r = await fetch('/convert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inp.value })
    });
    out.value = (await r.json()).json;
  }, 150);
});
</script>
</body>
</html>"""


def coerce(v):
    v = v.strip()
    # "str" prefix forces a string, e.g. str20 -> "20"
    if v.lower().startswith("str"):
        return v[3:]
    low = v.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low == "null":
        return None
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        pass
    return v


@app.route("/")
def index():
    return HTML


@app.route("/convert", methods=["POST"])
def convert():
    text = request.get_json(force=True).get("text", "")
    obj = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        if k:
            obj[k] = coerce(v)
    return jsonify({"json": json.dumps(obj, indent=2, ensure_ascii=False)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
