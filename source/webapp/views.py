from webapp.models import Food, Order
from django.views.generic import DetailView


class FoodDetailView(DetailView):
    model = Food
    template_name = 'food_detail.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
