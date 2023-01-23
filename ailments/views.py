from rest_framework.viewsets import ModelViewSet
from .models import Ailment, AilmentItem
from .serializers import AilmentSerializer


class AilmentViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Ailment.objects.all()
    serializer_class = AilmentSerializer
    search_fields = ['title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'request': self.request,
            'view': self
        })
        return context
