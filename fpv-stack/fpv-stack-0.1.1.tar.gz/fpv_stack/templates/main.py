template = """import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    return {{
        'message': 'Hello world!',
    }}


def start_dev() -> None:
    uvicorn.run(
        '{project_name}.main:app',
        host='0.0.0.0',
        port=8080,
        reload=True,
        workers=2,
    )
"""
