from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Photo(models.Model):
    imageId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    image = models.ImageField(upload_to='uploads/',default='')   
    Uploadtimestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Image {self.imageId}  at {self.Uploadtimestamp}"

class Caption(models.Model):
    captionId = models.AutoField(primary_key=True)
    image = models.ForeignKey(Photo, on_delete=models.CASCADE)
    captiontext = models.TextField()
    captionTimestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Caption {self.captionId} for Image {self.image.imageId} created at {self.captionTimestamp}"

