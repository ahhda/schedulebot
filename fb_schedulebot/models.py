from django.db import models

# Create your models here.
class fb_user(models.Model):
    fb_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)
    current_day = models.IntegerField(default=0)
    label = models.IntegerField(default=0)
    first_message = models.IntegerField(default=0)

    def __unicode__(self): # __str__ for Python 3, __unicode__ for Python 2
    	return self.first_name + " " + self.last_name