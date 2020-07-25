from django.db import models
from django.utils import timezone


class TelegramMessage(models.Model):
    update_id = models.CharField(max_length=255, blank=True)
    json_msg = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "TelegramMessages"
        ordering = ("update_id", "created_on")

    def __str__(self):
        return "{}".format(self.update_id)
