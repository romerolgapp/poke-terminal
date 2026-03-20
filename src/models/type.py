RESET = "\x1b[0m"


def _fg(r: int, g: int, b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"


def _bg(r: int, g: int, b: int) -> str:
    return f"\x1b[48;2;{r};{g};{b}m"


def _badge(icon: str, fg_rgb: tuple[int, int, int], bg_rgb: tuple[int, int, int]) -> str:
    fr, fg, fb = fg_rgb
    br, bg, bb = bg_rgb
    return f"{_fg(fr, fg, fb)}{_bg(br, bg, bb)} {icon} {RESET}"


TYPE_BADGES = {
    "normal": _badge("✴", (34, 34, 34), (168, 167, 122)),
    "fire": _badge("㊋", (255, 244, 214), (238, 129, 48)),
    "water": _badge("㊌", (240, 248, 255), (99, 144, 240)),
    "electric": _badge("ϟ", (56, 44, 0), (247, 208, 44)),
    "grass": _badge("☘", (248, 255, 240), (122, 199, 76)),
    "ice": _badge("❅", (30, 50, 70), (150, 217, 214)),
    "fighting": _badge("☯", (255, 245, 245), (194, 46, 40)),
    "poison": _badge("🌢", (255, 245, 250), (133, 12, 189)),
    "ground": _badge("⏚", (65, 45, 20), (226, 191, 101)),
    "flying": _badge("༄", (250, 250, 255), (169, 143, 243)),
    "psychic": _badge("❂", (255, 245, 0), (249, 85, 135)),
    "bug": _badge("⁂ ", (245, 255, 220), (166, 185, 26)),
    "rock": _badge("⼭", (255, 250, 240), (182, 161, 54)),
    "ghost": _badge("⚉", (248, 240, 255), (115, 87, 151)),
    "dragon": _badge("中", (245, 240, 255), (111, 53, 252)),
    "dark": _badge("☽", (245, 245, 245), (112, 87, 70)),
    "steel": _badge("㊎", (35, 45, 55), (183, 183, 206)),
    "fairy": _badge("❤", (255, 250, 255), (214, 133, 173)),
}


def render_type_badge(type_name: str) -> str:
    return TYPE_BADGES.get(type_name.lower(), type_name)
