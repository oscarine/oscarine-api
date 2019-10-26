from dotenv import load_dotenv
import os

load_dotenv()

API_V1_STR = "/api/v1"
BACKEND_CORS_ORIGINS = os.getenv(
    "BACKEND_CORS_ORIGINS"
)  # a string of origins separated by commas, e.g: "http://localhost, http://localhost:4200, http://localhost:3000, http://localhost:8080, http://local.dockertoolbox.tiangolo.com"
PROJECT_NAME = os.getenv("PROJECT_NAME")
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
