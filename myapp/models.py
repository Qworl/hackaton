from django.db import models

class Record(models.Model):
    id = models.BigAutoField
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name