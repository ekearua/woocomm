from django.urls import path, include
from rest_framework import serializers, viewsets, routers
from .models import Orders
from . import views

app_name = 'orders'

class OperatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_id','order_first_name','order_last_name','order_product','order_product_quantity','order_amount','order_address','order_delivery_type','order_delivery_date','lat','lon','order_payment_confirmation','order_status']

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
    path('update/<int:pk>/',views.update_order,name='update'),
    path('db/',views.UpdateDB.as_view(),name='webhook'),
    path('acc_update/<int:pk>',views.get_acc_order,name='acc_order'),
    path('del_update/<int:pk>',views.get_del_order,name='del_order'),
    path('pack_update/<int:pk>',views.get_pack_order,name='pack_order'),
    path('shopadmin_update/<int:pk>',views.get_shopadmin_order,name='shop_admin'),
    path('process-returns/',views.process_request,name='process_request'),
    path('returns/<int:pk>/',views.ReturnDetail.as_view(),name='return_detail'),
    path('returns/',views.ReturnList.as_view(),name='returns'),
    path('create_coupon/<int:pk>',views.create_coupon,name='create_coupon'),
    path('del-returns/<int:pk>/',views.get_del_return,name='del_return'),
    path('acc-returns/<int:pk>/',views.get_acc_return,name='acc_return'),
    path('pack-returns/<int:pk>/',views.get_pack_return,name='pack_return'),
    path('shop_admin_returns/<int:pk>',views.get_shopadmin_return,name='shopadmin_return')
]
