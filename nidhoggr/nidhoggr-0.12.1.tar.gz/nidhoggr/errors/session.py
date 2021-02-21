from nidhoggr.errors.common import YggdrasilError

InvalidServer = YggdrasilError(
    status=400,
    errorMessage="Wrong server identifier",
)
