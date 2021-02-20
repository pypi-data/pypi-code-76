from fastapi import FastAPI

def inject_health_check_api(app:FastAPI, health_check_name = 'health_check'):
    @app.get(f"/{health_check_name}")
    async def health_check():
        return {}
    