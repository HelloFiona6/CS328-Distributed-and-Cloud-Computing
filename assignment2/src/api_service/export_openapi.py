from fastapi.openapi.utils import get_openapi
from server import app
import yaml

def generate_openapi_yaml():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version if hasattr(app, "version") else "1.0.0",
        routes=app.routes,
    )

    with open("openapi.yaml", "w", encoding="utf-8") as f:
        yaml.dump(openapi_schema, f, sort_keys=False, allow_unicode=True)

    print("✅ openapi.yaml generated in src/api_service/openapi.yaml")

if __name__ == "__main__":
    generate_openapi_yaml()
