from flask_restx import Api
from app.config import Config
from app.api.data import data_ns


api = Api(
    version=Config.API_VERSION_V1, 
    title=Config.API_TITLE, 
    description=Config.APP_DESCRIPTION
)

v1_version_prefix = "/" + Config.API_VERSION_V1

api.add_namespace(data_ns, path=f"{v1_version_prefix}/api/data")
