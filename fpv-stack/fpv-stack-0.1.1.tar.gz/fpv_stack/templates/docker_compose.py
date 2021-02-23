template = '''version: "3"

services:
  {project_name}:
    build: .
    command: poetry run start_dev
    volumes:
      - .:/{project_name}
    ports:
      - 8080:8080'''
