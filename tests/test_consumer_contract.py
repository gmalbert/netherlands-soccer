from pathlib import Path

from config import LEAGUE_CONFIG
from pitch_oracle_core import __version__
from scripts.precompute_predictions import _weather_enabled


ROOT = Path(__file__).resolve().parents[1]
CORE_REF = "v1.3.16"


def test_consumer_selects_a_registered_non_epl_league():
    assert LEAGUE_CONFIG.key == "eredivisie"
    assert LEAGUE_CONFIG.key != "epl"
    assert LEAGUE_CONFIG.football_data_div
    assert LEAGUE_CONFIG.espn_slug


def test_core_pin_is_synchronized_everywhere():
    assert __version__ == CORE_REF.removeprefix("v")
    ci_pin = f"pitch-oracle-core[consumer] @ git+https://github.com/gmalbert/pitch-oracle-core.git@{CORE_REF}"
    assert ci_pin in (ROOT / "requirements.txt").read_text()
    assert ci_pin in (ROOT / "requirements-ci.txt").read_text()
    workflow = (ROOT / ".github" / "workflows" / "artifact-pipeline.yml").read_text()
    assert f"precompute-consumer.yml@{CORE_REF}" in workflow
    assert f"core_ref: {CORE_REF}" in workflow
    assert "secrets: inherit" in workflow


def test_local_secret_and_model_audit_contracts_are_present():
    ignore = (ROOT / ".gitignore").read_text()
    bootstrap = (ROOT / "scripts" / "bootstrap_local.py").read_text()

    assert ".env" in ignore
    assert (ROOT / ".env.example").is_file()
    assert 'load_dotenv(ROOT / ".env"' in bootstrap
    assert '"-m", "pitch_oracle_core.audit_cli"' in bootstrap


def test_prediction_weather_can_be_disabled(monkeypatch):
    monkeypatch.setenv("PITCH_ORACLE_DISABLE_WEATHER", "1")
    assert not _weather_enabled()

    monkeypatch.delenv("PITCH_ORACLE_DISABLE_WEATHER")
    assert _weather_enabled()
