"""Errors for Yggdrasil protocol"""

from nidhoggr.errors.common import YggdrasilError

MigrationDone = YggdrasilError(
    status=403,
    errorMessage="Use e-mail instead of plain login",
    cause="UserMigratedException",
)
InvalidCredentials = YggdrasilError(
    status=403,
    error="ForbiddenOperationException",
    errorMessage="Invalid credentials. Invalid username, email or password",
)
InvalidAccessToken = YggdrasilError(
    status=403,
    error="ForbiddenOperationException",
    errorMessage="accessToken expired or not exists",
)
InvalidClientToken = YggdrasilError(
    status=403,
    error="ForbiddenOperationException",
    errorMessage="Collision with clientToken, or it's broken",
)
InvalidProfile = YggdrasilError(
    status=400,
    errorMessage="Can't use selected profile",
)
