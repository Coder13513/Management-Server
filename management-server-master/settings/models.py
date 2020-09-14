from django.db import models

# Create your models here.

class Home(models.Model):
    home_page_url = models.URLField()
    site_title = models.CharField(max_length=255, blank=True, null=True)
    site_description = models.TextField(blank=True, null=True)
    site_logo = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.site_title

    def __unicode__(self):
        return self.site_title

    class Meta:
        verbose_name_plural = "Home Settings"
