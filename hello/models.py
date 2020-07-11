from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class imggal(models.Model):
    imgtitle = models.CharField(max_length=100)
    imgdesc = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images/")

