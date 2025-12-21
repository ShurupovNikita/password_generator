from flask import Flask, jsonify, render_template, request

from src import checker

app = Flask(__name__)
print("[DEBUG] Flask-приложение инициализировано")


@app.route("/")
def index():
    print("[DEBUG] GET / (UI)")
    return render_template("index.html")


@app.post("/api/check")
def api_check():
    payload = request.get_json(silent=True) or {}
    password = payload.get("password", "")
    print(f"[DEBUG] POST /api/check: получен пароль длиной {len(password)}")
    result = checker.score_password(password)
    print(f"[DEBUG] POST /api/check: расчёт завершён, балл={result['score']}, уровень={result['level']}")
    return jsonify(result)


@app.post("/api/generate")
def api_generate():
    payload = request.get_json(silent=True) or {}
    length = payload.get("length", 16)
    try:
        length = int(length)
    except (TypeError, ValueError):
        length = 16

    flags = {
        "use_lower": payload.get("lower", True),
        "use_upper": payload.get("upper", True),
        "use_digits": payload.get("digits", True),
        "use_symbols": payload.get("symbols", True),
    }
    try:
        password = checker.generate_password(length=length, **flags)
    except ValueError as exc:
        print(f"[DEBUG] POST /api/generate: ошибка {exc}")
        return jsonify({"error": str(exc)}), 400

    print(f"[DEBUG] POST /api/generate: сгенерирован пароль длиной {len(password)}")
    return jsonify({"password": password})


@app.get("/health")
def health():
    print("[DEBUG] GET /health")
    return {"status": "ok"}


if __name__ == "__main__":
    print("[DEBUG] Старт приложения Flask (debug=False)")
    app.run(host="0.0.0.0", port=8080, debug=False)
