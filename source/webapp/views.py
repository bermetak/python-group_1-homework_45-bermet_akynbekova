from django.views.generic import DetailView, CreateView, UpdateView, View, DeleteView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood, Employee
from webapp.forms import FoodForm, OrderForm, OrderFoodForm


class FoodDetailView(DetailView):
    model = Food
    template_name = 'food_detail.html'


class FoodCreateView(CreateView):
    model = Food
    template_name = 'food_create.html'
    form_class = FoodForm

    def get_success_url(self):
        return reverse('food_detail', kwargs={'pk': self.object.pk})



class UserListView(ListView):
    model = Employee
    template_name = 'user_list.html'

class FoodListView(ListView):
    model = Food
    template_name = 'food_list.html'

class FoodUpdateView(UpdateView):
    model = Food
    template_name = 'food_update.html'
    form_class = FoodForm

    def get_success_url(self):
        return reverse('food_detail', kwargs={'pk': self.object.pk})

class FoodDeleteView(DeleteView):
    model = Food
    template_name = 'food_delete.html'

    def get_success_url(self):
        return reverse ('food_list')



class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'

class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'

class OrderCancelView(View):
    model = Order
    template_name = 'order_cancel.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'order_cancel.html', {'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = 'canceled'
        order.save()
        return redirect('order_list')

class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


# Варианты представления для курьеров (взять заказ/доставить заказ)
# (в коде оставьте один)
# обычное - представление-функция
def order_deliver_view(request, *args, **kwargs):
    # найти заказ
    # если статус "Готовится", то
        # поменять статус на "В пути"
    # если статус "В пути", то
        # поменять статус на "Доставлено"
    # сохранить заказ
    # сделать редирект на список заказов
    pass


# классовое на базе View
class OrderDeliverView(View):
    model = Order
    template_name = 'order_deliver.html'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status == 'preparing':
            order.status = 'on_way'
        elif order.status == 'on_way':
            order.status = 'delivered'
        order.save()
        return redirect('order_list')

    #
    #
    # def post(self, request, pk):
    #     order = get_object_or_404(Order, pk=pk)
    #     order.status = 'STATUS_CANCELED'
    #     order.save()
    #     return redirect('order_list')


class OrderFoodCreateView(CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.order.pk})

class OrderFoodDeleteView(DeleteView):
    model = OrderFood
    template_name = 'order_food_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_food'] = OrderFood.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order_food = OrderFood.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.order.pk})
