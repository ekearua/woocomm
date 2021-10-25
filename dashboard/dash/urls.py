from django.urls import path, include
from rest_framework import serializers, viewsets, routers
from .models import Orders
from . import views

app_name = 'orders'

class OperatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_payment_confirmation']

class OperatorViewset(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OperatorSerializer

router = routers.DefaultRouter()
router.register(r'',OperatorViewset)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('',views.OrderList.as_view(),name='all'),
    path('<int:pk>/',views.OrderDetail.as_view(),name='single'),
    path('update/<int:pk>/',views.OrderUpdate.as_view(),name='update'),
    path('db',views.UpdateDB.as_view(),name='webhook')
]