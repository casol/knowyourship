from haystack import indexes
from .models import ShipList


class ShipListIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    ship = indexes.CharField(model_attr='ship')
    country = indexes.CharField(model_attr='country')

    def get_model(self):
        return ShipList

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
