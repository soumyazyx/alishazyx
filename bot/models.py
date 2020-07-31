from django.db import models
from django.utils import timezone


class TelegramMessage(models.Model):
    update_id = models.IntegerField()
    json_msg = models.TextField(blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    from_id = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "TelegramMessages"
        ordering = ("update_id", "created_on")

    def __str__(self):
        return "{}".format(self.update_id)
