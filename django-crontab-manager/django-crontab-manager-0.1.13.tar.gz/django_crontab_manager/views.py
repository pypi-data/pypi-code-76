import bizerror

from django.utils import timezone

from django_apiview.views import apiview

from .models import Result
from .models import Server
from .models import Schedule


def aclkey_check(server, aclkey):
    try:
        server = Server.objects.get(uid=server)
    except Server.DoesNotExist:
        raise bizerror.AppAuthFailed()
    if server.aclkey != aclkey:
        raise bizerror.AppAuthFailed()
    return server

@apiview
def getServerSettings(server, aclkey):
    server = aclkey_check(server, aclkey)
    # update server's update time.
    server.last_updated_time = timezone.now()
    server.save()
    # if server NOT enabled, disable all schedules.
    if not server.enable:
        return {}
    # get all schedules' code.
    result = {}
    for schedule in Schedule.objects.filter(server=server):
        result[str(schedule.uid)] = schedule.code
    return result

@apiview
def getScheduleSettings(server, aclkey, schedule):
    server = aclkey_check(server, aclkey)
    schedule = Schedule.objects.get(uid=schedule)
    return schedule.info()

@apiview
def reportRunResult(server, aclkey, schedule, run_time=None, code=None, stdout=None, stderr=None):
    server = aclkey_check(server, aclkey)
    schedule = Schedule.objects.get(uid=schedule)
    result = Result()
    result.schedule = schedule
    result.run_time = run_time or timezone.now()
    result.code = code
    result.stdout = stdout
    result.stderr = stderr
    result.save()
    return True
