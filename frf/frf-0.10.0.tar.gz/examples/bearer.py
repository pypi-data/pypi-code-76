# pylint: skip-file
#
# Do not put more than one class in a file, this is for example purposes
# only.
import os
from typing import Optional

import ioc
import frf
import uvicorn
from pydantic import BaseModel
from unimatrix.ext.model import Repository


class Subject(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class SubjectRepository(Repository):
    subjects = {
        "johndoe": {
            "username": "johndoe",
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "secret": "secret_for_john",
            "disabled": False,
        },
        "alice": {
            "username": "alice",
            "full_name": "Alice Wonderson",
            "email": "alice@example.com",
            "secret": "secret_for_alice",
            "disabled": True,
        },
    }

    async def get(self, username):
        return Subject(**self.subjects[username])


class BearerSubjectResolver(frf.BearerSubjectResolver):

    @frf.inject('subjects', 'SubjectRepository')
    async def get_subject(self, claims, subjects):
        return await subjects.get(claims['sub'])


class ProtectedResource(frf.Resource):

    async def list(self, subject=frf.CurrentSubject):
        return {
            "message": (
                f"Hello, {subject.full_name}. "
                "You succesfully accessed the protected resource!"
            )
        }


app = frf.get_asgi_application(allowed_hosts=['*'])
app.add_resource(ProtectedResource)

@app.on_event('startup')
async def boot():
    frf.provide('SubjectRepository', SubjectRepository())
    frf.provide('BearerSubjectResolver', BearerSubjectResolver(), force=True)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
