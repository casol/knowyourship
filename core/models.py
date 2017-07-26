from django.db import models


class ShipList(models.Model):
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


class ShipImage(models.Model):
    """Model responsible for storing images."""
    title = models.CharField(max_length=200)
    image_description = models.TextField(blank=True)
    artist = models.CharField(max_length=200)
    data = models.CharField()
    url = models.URLField()
    slug = models.SlugField(max_length=200, blank=True)
    usage_terms = models.CharField(max_length=250)
    license_url = models.URLField()
    license_short_name = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class ShipDetails(models.Model):
    content = models.TextField(blank=True)





