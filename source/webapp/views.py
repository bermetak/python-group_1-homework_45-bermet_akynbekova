from django.views.generic import DetailView, CreateView, UpdateView, View, DeleteView, ListView
from django.urls import reverse
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

class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'

class UserListView(ListView):
    model = Employee
    template_name = 'user_list.html'



class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'


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
    def get(self, *args, **kwargs):
        # найти заказ
        # если статус "Готовится", то
            # поменять статус на "В пути"
        # если статус "В пути", то
            # поменять статус на "Доставлено"
        # сохранить заказ
        # сделать редирект на список заказов
        pass


# Варианты представления для отмены заказов
# (в коде оставьте один)
# обычное - представление-функция
def order_reject_view(request, *args, **kwargs):
    # найти заказ
    # поменять статус на canceled
    # сохранить заказ
    # сделать редирект на список заказов
    pass


# классовое на базе View
class OrderRejectView(View):
    def get(self, *args, **kwargs):
        # найти заказ
        # поменять статус на canceled
        # сохранить заказ
        # сделать редирект на список заказов
        pass


# классовое на базе DeleteView с выводом страницы подтверждения
class OrderRejectViewV2(DeleteView):
    model = OrderUpdateView
    template_name = 'order_cancel.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        # поменять статус на canceled
        # сохранить заказ
        return HttpResponseRedirect(success_url)


# Представления для создания заказа
class OrderCreateView(CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.pk})


# ... и для добавления блюд в заказ
class OrderFoodCreateView(CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'

    def get_success_url(self):
        return reverse('order_detail', kwargs={'pk': self.object.order.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    # Здесь нужен метод get_form_valid, который будет добавлять
    # в объект OrderFood из формы ссылку на заказ
    # по примеру из вебинара для бонуса в дз #43.


class OrderFoodDeleteView(DeleteView):
    # Доработайте это представление (удаление блюда из заказа).
    # В шаблоне вы также не должны выводить форму, как и в order_food_create.html
    # Если статус заказа - доставлен или в пути

    model = OrderFood
