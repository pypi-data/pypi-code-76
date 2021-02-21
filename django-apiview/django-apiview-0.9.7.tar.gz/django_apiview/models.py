

from fastutils import dictutils

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class ApiResponseTimeLog(models.Model):
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Add Time"))
    path = models.CharField(max_length=128, verbose_name=_("Api Path"))
    response_time = models.IntegerField(verbose_name=_("Response Time"), help_text=_("Response time in microsecond. 1,000,000 microseconds == 1 second."))

    class Meta:
        verbose_name = _("Api Response Time Log")
        verbose_name_plural = _("Api Response Time Logs")

    def __str__(self):
        return str(self.pk)


class ApiResponseTimeStats(models.Model):
    path = models.CharField(max_length=128, verbose_name=_("Api Path"), unique=True)
    count = models.IntegerField(verbose_name=_("Count"))
    min_response_time = models.IntegerField(verbose_name=_("Min Response Time"))
    avg_response_time = models.IntegerField(verbose_name=_("Avg Response Time"))
    max_response_time = models.IntegerField(verbose_name=_("Max Response Time"))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_("Last Update Time"))

    class Meta:
        verbose_name = _("Api Response Time Stats")
        verbose_name_plural = _("Api Response Time Stats")
    
    def __str__(self):
        return self.path

    @classmethod
    def update(cls):
        old_stats = {}
        for stat in cls.objects.all():
            old_stats[stat.path] = stat

        stats = ApiResponseTimeLog.objects.all().values("path").annotate(
            count=models.Count("path"),
            min_response_time=models.Min("response_time"),
            avg_response_time=models.Avg("response_time"),
            max_response_time=models.Max("response_time"),
        )

        now = timezone.now()
        created_stats = []
        updated_stats = []
        new_path = set()
        for info in stats:
            path = info["path"]
            info["count"] = int(info["count"])
            info["min_response_time"] = int(info["min_response_time"])
            info["avg_response_time"] = int(info["avg_response_time"])
            info["max_response_time"] = int(info["max_response_time"])
            new_path.add(path)
            if path in old_stats:
                stat = old_stats[path]
                updated = dictutils.changes(stat, info, ["count", "min_response_time", "avg_response_time", "max_response_time"])
                if updated:
                    stat.update_time = now
                    updated_stats.append(stat)
            else:
                stat = cls()
                stat.path = path
                stat.count = info["count"]
                stat.min_response_time = info["min_response_time"]
                stat.avg_response_time = info["avg_response_time"]
                stat.max_response_time = info["max_response_time"]
                created_stats.append(stat)

        cls.objects.bulk_create(created_stats)
        cls.objects.bulk_update(updated_stats, fields=["count", "min_response_time", "avg_response_time", "max_response_time", "update_time"])
        deleted_stats_ids = []
        for path, stat in old_stats.items():
            if not path in new_path:
                deleted_stats_ids.append(stat.pk)
        cls.objects.filter(pk__in=deleted_stats_ids).delete()

        return {
            "created_count": len(created_stats),
            "updated_count": len(updated_stats),
            "deleted_count": len(deleted_stats_ids)
        }
