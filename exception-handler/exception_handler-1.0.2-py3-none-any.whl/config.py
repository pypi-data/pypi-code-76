from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    environments=True,
    load_dotenv=True,
    includes=["../app/settings.toml"],
    settings_files=["settings.toml", "../app/settings.toml"],
    validators=[
        Validator("LOG_LEVEL", must_exist=True),
        Validator("LOG_BACKTRACE", must_exist=True),
        Validator("DIAGNOSE", must_exist=True),
    ]
)
