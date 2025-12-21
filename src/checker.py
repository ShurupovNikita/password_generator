import math
import re
import secrets
import string

COMMON_PASSWORDS = {
    "123456",
    "password",
    "qwerty",
    "123456789",
    "12345678",
    "111111",
    "1234567",
    "sunshine",
    "iloveyou",
    "princess",
    "admin",
    "welcome",
}

CHAR_CLASSES = {
    "lower": r"[a-z]",
    "upper": r"[A-Z]",
    "digit": r"[0-9]",
    "symbol": r"[^A-Za-z0-9]",
}

GEN_CHARSETS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digit": string.digits,
    "symbol": "!@#$%^&*()-_=+[]{};:,.?/|",
}


def estimate_entropy(password: str) -> float:
    """Простая оценка энтропии: суммируем разные наборы символов и длину."""
    pool = 0
    if re.search(CHAR_CLASSES["lower"], password):
        pool += 26
    if re.search(CHAR_CLASSES["upper"], password):
        pool += 26
    if re.search(CHAR_CLASSES["digit"], password):
        pool += 10
    if re.search(CHAR_CLASSES["symbol"], password):
        pool += 32  # прибл.
    if pool == 0:
        return 0.0
    entropy = math.log2(pool) * len(password)
    return entropy


def score_password(password: str) -> dict:
    """Возвращает оценку и рекомендации."""
    print(f"[DEBUG] score_password: старт расчёта, длина пароля={len(password) if password else 0}")
    if password is None:
        password = ""

    results = {
        "length": len(password),
        "contains_lower": bool(re.search(CHAR_CLASSES["lower"], password)),
        "contains_upper": bool(re.search(CHAR_CLASSES["upper"], password)),
        "contains_digit": bool(re.search(CHAR_CLASSES["digit"], password)),
        "contains_symbol": bool(re.search(CHAR_CLASSES["symbol"], password)),
        "is_common": password.lower() in COMMON_PASSWORDS,
        "entropy": estimate_entropy(password),
    }

    # баллы по правилам (0-100)
    score = 0
    # длина
    if results["length"] >= 12:
        score += 35
    elif results["length"] >= 8:
        score += 20
    elif results["length"] >= 6:
        score += 10

    # разнообразие символов
    classes = sum(
        [
            results["contains_lower"],
            results["contains_upper"],
            results["contains_digit"],
            results["contains_symbol"],
        ]
    )
    score += min(classes * 15, 45)

    # общие пароли — большой штраф
    if results["is_common"]:
        score = max(score - 50, 0)

    # бонус за высокую энтропию
    if results["entropy"] >= 60:
        score = min(score + 10, 100)

    results["score"] = int(score)

    # уровень
    if score >= 80:
        level = "сильный"
    elif score >= 50:
        level = "средний"
    else:
        level = "слабый"
    results["level"] = level

    # рекомендации
    recs = []
    if results["is_common"]:
        recs.append("Пароль встречается в списках распространённых паролей — замените.")
    if results["length"] < 12:
        recs.append("Увеличьте длину пароля до 12 и более символов.")
    if not results["contains_upper"]:
        recs.append("Добавьте заглавные буквы (A-Z).")
    if not results["contains_lower"]:
        recs.append("Добавьте строчные буквы (a-z).")
    if not results["contains_digit"]:
        recs.append("Добавьте цифры (0-9).")
    if not results["contains_symbol"]:
        recs.append("Добавьте символы (например: !@#%&*).")
    if not recs:
        recs.append("Пароль выглядит хорошо, но проверьте уникальность и храните его в менеджере паролей.")
    results["recommendations"] = recs

    print(
        f"[DEBUG] score_password: итоговые баллы={results['score']}, "
        f"уровень={results['level']}, энтропия={results['entropy']:.1f}"
    )
    return results


def generate_password(
    length: int = 16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """Генерирует пароль заданной длины по выбранным классам символов."""
    print(
        f"[DEBUG] generate_password: длина={length}, lower={use_lower}, "
        f"upper={use_upper}, digits={use_digits}, symbols={use_symbols}"
    )
    if length < 4:
        length = 4
    if length > 128:
        length = 128

    pools = []
    if use_lower:
        pools.append(GEN_CHARSETS["lower"])
    if use_upper:
        pools.append(GEN_CHARSETS["upper"])
    if use_digits:
        pools.append(GEN_CHARSETS["digit"])
    if use_symbols:
        pools.append(GEN_CHARSETS["symbol"])

    if not pools:
        raise ValueError("Нужно выбрать хотя бы один набор символов")

    # гарантируем минимум по одному символу из каждого выбранного набора
    password_chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    remaining = length - len(password_chars)
    password_chars.extend(secrets.choice(all_chars) for _ in range(max(remaining, 0)))

    secrets.SystemRandom().shuffle(password_chars)
    generated = "".join(password_chars)[:length]
    print(f"[DEBUG] generate_password: готово, длина={len(generated)}")
    return generated
