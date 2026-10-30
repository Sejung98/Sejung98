"""Generate the tech-stack strip and project cards (dark/light) into assets/.

Run: python build_assets.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(card="#161b22", border="#30363d", fg="#e6edf3", muted="#8b949e", accent="#58a6ff"),
    "light": dict(card="#f6f8fa", border="#d0d7de", fg="#1f2328", muted="#59636e", accent="#0969da"),
}

STACK = [
    ("claude", "Claude"),
    ("python", "Python"),
    ("r", "R"),
    ("nextflow", "Nextflow"),
    ("linux", "Linux"),
    ("gnubash", "Bash"),
    ("docker", "Docker"),
]

# (repo, description lines, language, language color)
PROJECTS = [
    ("WGS-Germline-pipeline-nf",
     ["Whole-genome germline analysis pipeline", "on Nextflow, built on the Hartwig pipeline"],
     "Nextflow", "#3ac486"),
    ("WGS_HMF",
     ["Whole-genome sequencing analysis based on", "the Hartwig Medical Foundation toolkit"],
     "Java", "#b07219"),
    ("follow_wollof",
     ["Tracks research sessions with Claude", "as a live progress graph"],
     "Python", "#3572A5"),
    ("paper-surfer",
     ["Finds and ranks research papers", "from PubMed"],
     "Python", "#3572A5"),
]


def icon_path(name):
    svg = (ASSETS / "icons" / f"{name}.svg").read_text(encoding="utf-8")
    return re.search(r'<path d="([^"]+)"', svg).group(1)


def stack_svg(t):
    # 6px side inset matches the project cards' left/right edges
    w, h, gap, n, inset = 1000, 128, 12, len(STACK), 6
    cw = (w - 2 * inset - gap * (n - 1)) / n
    cells = []
    for i, (slug, label) in enumerate(STACK):
        x = inset + i * (cw + gap)
        cx = x + cw / 2
        cells.append(
            f'<rect x="{x + 0.5:.1f}" y="0.5" width="{cw - 1:.1f}" height="{h - 1}" rx="12" '
            f'fill="{t["card"]}" stroke="{t["border"]}"/>'
            f'<path transform="translate({cx - 18:.1f} 26) scale(1.5)" fill="{t["fg"]}" d="{icon_path(slug)}"/>'
            f'<text x="{cx:.1f}" y="100" text-anchor="middle" font-size="15" fill="{t["muted"]}">{label}</text>'
        )
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">'
            + "".join(cells) + "</svg>")


def card_svg(t, repo, lines, lang, lang_color):
    # 6px inset so two cards placed edge to edge get a 12px gutter
    desc = "".join(
        f'<text x="30" y="{80 + i * 22}" font-size="15" fill="{t["muted"]}">{s}</text>'
        for i, s in enumerate(lines)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 170" font-family="{FONT}">'
        f'<rect x="6.5" y="6.5" width="487" height="157" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>'
        f'<text x="30" y="48" font-size="19" font-weight="600" fill="{t["accent"]}">{repo}</text>'
        f"{desc}"
        f'<circle cx="36" cy="138" r="6" fill="{lang_color}"/>'
        f'<text x="50" y="143" font-size="14" fill="{t["muted"]}">{lang}</text>'
        "</svg>"
    )


def main():
    for theme, t in THEMES.items():
        (ASSETS / f"stack-{theme}.svg").write_text(stack_svg(t), encoding="utf-8")
        for repo, lines, lang, color in PROJECTS:
            (ASSETS / f"card-{repo}-{theme}.svg").write_text(
                card_svg(t, repo, lines, lang, color), encoding="utf-8")


if __name__ == "__main__":
    main()
