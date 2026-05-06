from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    catch_phrase = models.TextField(blank=True)
    bs = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Companies"
    
    def __str__(self):
        return self.name

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True)
    suite = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, db_index=True)
    zipcode = models.CharField(max_length=50, blank=True)
    lat = models.CharField(max_length=50, blank=True)
    lng = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.street}, {self.city}"

class User(models.Model):
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, db_index=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    website = models.CharField(max_length=255, blank=True)
    
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='users')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['external_id']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['external_id']),
        ]
    
    def __str__(self):
        return f"{self.name} (@{self.username})"