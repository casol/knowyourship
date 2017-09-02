from haystack import indexes
from .models import ShipList


class ShipListIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    # autocomplete with one field?
    # ship_auto = indexes.EdgeNgramField(model_attr='ship')
    # country_auto = indexes.EdgeNgramField(model_attr='country')

    def get_model(self):
        return ShipList

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
