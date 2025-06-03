from django.db import models
from django.contrib.auth.models import User

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Template Market")
    site_description = models.TextField(blank=True)
    maintenance_mode = models.BooleanField(default=False)
    contact_email = models.EmailField()
    
    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteConfiguration.objects.exists():
            # Only allow one instance of SiteConfiguration
            return
        return super(SiteConfiguration, self).save(*args, **kwargs)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.email}"

    class Meta:
        ordering = ['-created_at']
