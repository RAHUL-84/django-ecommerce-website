from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def register(self):
        self.save()

    def isExist(self):
        if Customer.objects.filter(phone=self.phone):
            return True
        else:
            return False