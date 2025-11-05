"""Configuration management using dynaconf."""

from pathlib import Path

from dynaconf import Dynaconf

# Get the project root directory
_current_file = Path(__file__).resolve()
_project_root = _current_file.parent.parent.parent

settings = Dynaconf(
    envvar_prefix="RTLLIB",
    settings_files=[str(_project_root / "config" / "settings.toml")],
    environments=True,
    load_dotenv=True,
    env_switcher="RTLLIB_ENV",
)
