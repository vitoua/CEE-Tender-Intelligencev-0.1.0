from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 database_url:str='sqlite:///./tenders.db'; secret_key:str='dev'; admin_email:str='admin@example.com'; admin_password:str='ChangeMe123!'; app_language:str='uk'
 model_config=SettingsConfigDict(env_file='.env',extra='ignore')
settings=Settings()
