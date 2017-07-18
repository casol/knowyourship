from django.db import models


class ListOfMuseumShips(models.Model):
    """List of museum ships."""
    ship = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    region = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    from_country = models.CharField(max_length=250)
    year = models.CharField(max_length=250)
    ship_class = models.CharField(max_length=250, blank=True)
    ship_type = models.CharField(max_length=250, blank=True)
    remarks = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.ship
