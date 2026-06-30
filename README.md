# txt2json
Converts key: value text into JSON.

#### Running

pip3 install flask

python3 app.py

http://localhost:5000

#### Usage

- One key: value per line:
  - name: John Doe
  - age: 25
  - email: john@doe.com

Types are detected automatically (true/false, null, int, float, string). Use the str prefix to force a string: code: str20 → "20".
