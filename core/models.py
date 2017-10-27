from django.db import models
from django.core.urlresolvers import reverse


class ShipList(models.Model):
    """Model of museum ships."""
    ship = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    region = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    from_country = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    ship_class = models.CharField(max_length=200, blank=True)
    ship_type = models.CharField(max_length=200, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=200)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse('core:ship_detail',
                       args=[self.slug])

    def __str__(self):
        return self.ship


class ShipImage(models.Model):
    """Model responsible for storing images."""
    ship = models.OneToOneField(ShipList, blank=True,
                                null=True, related_name='ship_image')
    image = models.ImageField(upload_to='images/',
                              blank=True,
                              null=True)
    title = models.CharField(max_length=200)
    image_description = models.TextField(blank=True)
    artist = models.CharField(max_length=200)
    created = models.CharField(max_length=200)
    source_url = models.URLField()
    slug = models.SlugField(max_length=200, blank=True)
    usage_terms = models.CharField(max_length=250)
    license_url = models.URLField()
    license_short_name = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class ShipDetails(models.Model):
    """Ship details description."""
    ship = models.OneToOneField(ShipList, related_name='details')
    content = models.TextField(blank=True)
    remarks = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.ship.ship


class ShipCoordinates(models.Model):
    """Ship geographic coordinate, for simplicity purpose model
    does not use GeoDjango and PostGIS.
    """
    ship = models.OneToOneField(ShipList, related_name='coordinates')
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return 'lat: {}, lng: {}'.format(self.latitude, self.longitude)


class Comment(models.Model):
    ship = models.ForeignKey(ShipList, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=200, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.ship)
