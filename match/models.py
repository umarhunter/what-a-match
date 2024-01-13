from django.db import models


class Person(models.Model):
    """A person with their respective preferences"""
    name = models.CharField(max_length=50)
    preferences = models.CharField(max_length=50)

    # date_added = models.DateTimeField(auto_now_add=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.name
