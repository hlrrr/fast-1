from pydantic   import BaseSettings

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    database_url: str
    database_url_alembic:str
    secrete_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_file = ".env"

settings = Settings()


class Settings_test(BaseSettings):
    database_hostname_test:str
    database_port_test:str
    database_password_test:str
    database_name_test:str
    database_username_test:str
    database_url_test: str
    database_url_alembic_test:str
    secrete_key_test:str
    algorithm_test:str
    access_token_expire_minutes_test:int

    class Config:
        env_file = ".env"

settings_test = Settings_test()