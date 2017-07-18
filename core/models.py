from django.db import models


class ListOfMuseumShips(models.Model):
    """List of museum ships."""
    ship = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    region = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    from_country = models.CharField(max_length=250)
    year = models.CharField(max_length=250)
    ship_class = models.CharField(max_length=250)
    ship_type = models.CharField(max_length=250)
    remarks = models.CharField(max_length=250)

    def __str__(self):
        return self.ship
