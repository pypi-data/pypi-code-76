# pylint: skip-file
from bearer import *


class BearerSubjectResolver(frf.BearerSubjectResolver):

    async def verify_signature(self, token):
      # Be aware that the signature of the Bearer token is not verified
      # yet, so the claims should not be trusted.
      signing_key = lookup_subject_key(token.get_unverified('sub'))
      return token.verify(signing_key=signing_key)


if __name__ == '__main__':
    frf.provide('SubjectRepository', SubjectRepository())
    frf.provide('BearerSubjectResolver', BearerSubjectResolver(), force=True)

    uvicorn.run('auth:app', host="127.0.0.1", port=8000, reload=True)
