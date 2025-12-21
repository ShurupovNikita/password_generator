import argparse

from src import checker


def main():
    print("[DEBUG] Запуск CLI проверки пароля")

    parser = argparse.ArgumentParser(description="Проверка надёжности пароля")
    parser.add_argument(
        "password",
        nargs="?",
        help="Пароль для проверки (если не указать, будет запрошен)",
    )
    args = parser.parse_args()

    if not args.password:
        print("[DEBUG] Пароль не передан аргументом, запрашиваем интерактивно")
        try:
            import getpass

            pw = getpass.getpass("Введите пароль: ")
        except Exception:
            pw = input("Введите пароль: ")
    else:
        print("[DEBUG] Пароль получен из аргумента командной строки")
        pw = args.password

    res = checker.score_password(pw)
    print(f"[DEBUG] Результат вычислений: длина={res['length']}, энтропия={res['entropy']:.1f}, балл={res['score']}")
    print("Анализ пароля:")
    print(f"  Длина: {res['length']}")
    print(f"  Энтропия (оценка): {res['entropy']:.1f} бит")
    print(f"  Балл: {res['score']} / 100")
    print(f"  Уровень: {res['level']}")
    print("  Рекомендации:")
    for r in res["recommendations"]:
        print(f"   - {r}")


if __name__ == "__main__":
    main()
