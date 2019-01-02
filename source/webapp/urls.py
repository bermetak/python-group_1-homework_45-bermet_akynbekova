from django.urls import path
from webapp.views import FoodDetailView, OrderDetailView, OrderCreateView, FoodCreateView, OrderUpdateView, \
    OrderFoodCreateView, OrderListView, UserListView, FoodListView, OrderCancelView, FoodUpdateView, FoodDeleteView, \
    OrderFoodDeleteView, OrderDeliverView, OrderFoodUpdateView

app_name = 'webapp'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('user', UserListView.as_view(), name='user_list'),
    path('food', FoodListView.as_view(), name='food_list'),
    path('food/<int:pk>', FoodDetailView.as_view(), name='food_detail'),
    path('food/<int:pk>/update', FoodUpdateView.as_view(), name='food_update'),
    path('food/<int:pk>/delete', FoodDeleteView.as_view(), name='food_delete'),
    path('food/create', FoodCreateView.as_view(), name='food_create'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order/create', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/cancel', OrderCancelView.as_view(), name='order_cancel'),
    path('order/<int:pk>/deliver', OrderDeliverView.as_view(), name='order_deliver'),
    path('order/<int:pk>/food/create', OrderFoodCreateView.as_view(), name='order_food_create'),
    path('order_food/<int:pk>/update', OrderFoodUpdateView.as_view(), name='order_food_update'),
    path('order_food/<int:pk>/delete', OrderFoodDeleteView.as_view(), name='order_food_delete')
]


