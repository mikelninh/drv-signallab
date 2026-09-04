from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

from .data import generate_cases
from .metrics import BASELINE_END, BASELINE_START, RECENT_START, detect_signals


def _de1(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def presentation_snapshot(df: pd.DataFrame | None = None) -> dict:
    """Return the exact values shown in the public work-sample UI.

    The snapshot is derived from the same deterministic dataset and signal engine used by
    the API. This prevents the portfolio presentation from drifting away from the analytics.
    """
    frame = generate_cases() if df is None else df
    signals = detect_signals(frame)
    signal = next(
        s
        for s in signals
        if s["process_type"] == "Kontenklaerung" and s["region"] == "Berlin"
    )

    target = frame[
        (frame.process_type == "Kontenklaerung") & (frame.region == "Berlin")
    ].copy()
    target["month"] = target.received_at.dt.to_period("M").astype(str)
    monthly = (
        target.groupby("month", observed=True)
        .agg(mean_days=("processing_days", "mean"))
        .reset_index()
    )
    values = [round(float(v), 1) for v in monthly.mean_days]

    return {
        "signal": signal,
        "chart_values": values,
        "chart_caption": (
            "24-Monats-Verlauf · Signalvergleich: Dez. 2025 – Mai 2026 vs. Juni – Aug. 2026"
        ),
        "baseline": {
            "start": str(BASELINE_START.date()),
            "end": str(BASELINE_END.date()),
        },
        "recent_start": str(RECENT_START.date()),
    }


def render_demo_html(source_html: str, faq_html: str, snapshot: dict | None = None) -> str:
    """Render the deployable static demo from the source template and engine snapshot."""
    snap = presentation_snapshot() if snapshot is None else snapshot
    signal = snap["signal"]
    html = source_html

    # Keep the first read focused on the user outcome, not methodology.
    long_hero = (
        "Die mittlere Bearbeitungszeit für Kontenklärungen in Berlin ist im letzten "
        "Beobachtungszeitraum deutlich gestiegen."
    )
    html = html.replace(long_hero, "Bearbeitungszeit bei Kontenklärungen deutlich gestiegen.", 1)

    # Present only values produced by the analytics engine.
    replacements = {
        r'<div class="metric">.*?</div>': (
            f'<div class="metric">{_de1(signal["baseline_days"])} → '
            f'{_de1(signal["recent_days"])} Tage</div>'
        ),
        r'<strong>\+.*? Tage</strong>': (
            f'<strong>+{_de1(signal["delta_days"])} Tage</strong>'
        ),
        r'<span class="dot">95%-KI .*?</span>': (
            f'<span class="dot">95%-KI +{_de1(signal["ci_95_low_days"])} bis '
            f'+{_de1(signal["ci_95_high_days"])} </span>'
        ),
        r'<span class="dot">\d+ aktuelle Fälle</span>': (
            f'<span class="dot">{signal["recent_n"]} aktuelle Fälle</span>'
        ),
        r'<div class="fact-row"><div>Stichprobe</div><div>.*?</div></div>': (
            '<div class="fact-row"><div>Stichprobe</div><div>'
            f'{signal["baseline_n"]} vs. {signal["recent_n"]} Fälle</div></div>'
        ),
        r'<div class="fact-row"><div>Effekt</div><div class="emph">.*?</div></div>': (
            '<div class="fact-row"><div>Effekt</div><div class="emph">'
            f'+{_de1(signal["delta_days"])} Tage</div></div>'
        ),
        r'<div class="fact-row"><div>95%-Konfidenzintervall</div><div>.*?</div></div>': (
            '<div class="fact-row"><div>95%-Konfidenzintervall</div><div>'
            f'+{_de1(signal["ci_95_low_days"])} bis +{_de1(signal["ci_95_high_days"])} Tage'
            '</div></div>'
        ),
        r'<div class="fact-row"><div>Effektstärke</div><div>.*?</div></div>': (
            '<div class="fact-row"><div>Effektstärke</div><div>Cohen’s d '
            f'{str(signal["effect_size"]).replace(".", ",")}</div></div>'
        ),
        r'<p class="chart-sub">.*?</p>': (
            f'<p class="chart-sub">{snap["chart_caption"]}</p>'
        ),
        r'const values = \[[^\]]*\];': (
            f'const values = {json.dumps(snap["chart_values"], ensure_ascii=False)};'
        ),
    }

    for pattern, replacement in replacements.items():
        html, count = re.subn(pattern, replacement, html, count=1, flags=re.S)
        if count != 1:
            raise ValueError(f"presentation anchor did not match exactly once: {pattern}")

    # Methodology remains available, but visually secondary.
    html = html.replace(
        '<h3>Methodik & technische Umsetzung</h3>',
        '<h3>Methodik</h3>',
        1,
    )

    anchor = '    <section class="panel method">'
    if anchor not in html:
        raise ValueError("FAQ injection anchor not found")
    html = html.replace(anchor, faq_html + "\n\n" + anchor, 1)
    return html


def build_demo(
    source: Path = Path("web/index.html"),
    faq: Path = Path("web/faq-snippet.html"),
    output: Path = Path("_site/index.html"),
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered = render_demo_html(
        source.read_text(encoding="utf-8"),
        faq.read_text(encoding="utf-8"),
    )
    output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    build_demo()
