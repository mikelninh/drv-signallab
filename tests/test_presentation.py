from pathlib import Path

from signallab.data import generate_cases
from signallab.presentation import presentation_snapshot, render_demo_html


def test_presentation_snapshot_matches_berlin_engine_signal():
    snapshot = presentation_snapshot(generate_cases())
    signal = snapshot["signal"]

    assert signal["process_type"] == "Kontenklaerung"
    assert signal["region"] == "Berlin"
    assert signal["baseline_days"] == 24.2
    assert signal["recent_days"] == 32.7
    assert signal["delta_days"] == 8.4
    assert signal["baseline_n"] == 921
    assert signal["recent_n"] == 410
    assert signal["ci_95_low_days"] == 7.7
    assert signal["ci_95_high_days"] == 9.1
    assert signal["effect_size"] == 1.45
    assert snapshot["chart_values"][-3:] == [33.0, 32.7, 32.2]


def test_rendered_demo_uses_engine_values_and_correct_signal_window():
    source = Path("web/index.html").read_text(encoding="utf-8")
    faq = Path("web/faq-snippet.html").read_text(encoding="utf-8")
    html = render_demo_html(source, faq, presentation_snapshot(generate_cases()))

    assert "24,2 → 32,7 Tage" in html
    assert "+8,4 Tage" in html
    assert "95%-KI +7,7 bis +9,1" in html
    assert "921 vs. 410 Fälle" in html
    assert "Cohen’s d 1,45" in html
    assert "24-Monats-Verlauf · Signalvergleich: Dez. 2025 – Mai 2026 vs. Juni – Aug. 2026" in html
    assert "const values = [24.4, 24.0, 24.5" in html
    assert "33.0, 32.7, 32.2]" in html


def test_rendered_demo_does_not_keep_stale_chart_values_or_caption():
    source = Path("web/index.html").read_text(encoding="utf-8")
    faq = Path("web/faq-snippet.html").read_text(encoding="utf-8")
    html = render_demo_html(source, faq)

    assert "30.8,33.0,34.3" not in html.replace(" ", "")
    assert "Vergleichszeitraum: Sept. 2024 – Mai 2026" not in html
