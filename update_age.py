"""Atualiza a idade (Uptime) no dark_mode.svg. Roda todo dia via GitHub Actions."""
import re
import sys
from datetime import date
from pathlib import Path

BIRTH = date(2001, 6, 8)   # 08/06/2001
W = 52                      # mesma largura de colunas usada no SVG
SVG = Path(__file__).parent / "dark_mode.svg"


def age_text(today: date) -> str:
    years = today.year - BIRTH.year - ((today.month, today.day) < (BIRTH.month, BIRTH.day))
    months = (today.month - BIRTH.month - (today.day < BIRTH.day)) % 12
    ym = BIRTH.year * 12 + (BIRTH.month - 1) + years * 12 + months
    anniversary = date(ym // 12, ym % 12 + 1, BIRTH.day)
    return f"{years} years, {months} months, {(today - anniversary).days} days"


def main() -> None:
    today = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    value = age_text(today)
    used = 2 + len("Uptime") + 1 + 1 + len(value) + 1
    dots = " " + "." * max(3, W - used) + " "

    text = SVG.read_text(encoding="utf-8")
    pattern = re.compile(
        r"""(<tspan class="cc" id=['"]age_data_dots['"]>)[^<]*(</tspan>"""
        r"""<tspan class="value" id=['"]age_data['"]>)[^<]*(</tspan>)"""
    )
    new_text, n = pattern.subn(lambda m: f"{m.group(1)}{dots}{m.group(2)}{value}{m.group(3)}", text)
    if n != 1:
        sys.exit("Não encontrei a linha do Uptime no SVG (age_data).")
    SVG.write_text(new_text, encoding="utf-8")
    print(f"Idade atualizada: {value}")


if __name__ == "__main__":
    main()
