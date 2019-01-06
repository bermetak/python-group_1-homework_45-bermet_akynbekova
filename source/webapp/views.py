from django.views.generic import DetailView, CreateView, UpdateView, View, DeleteView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from webapp.models import Food, Order, OrderFood, Employee
from webapp.forms import FoodForm, OrderForm, OrderFoodForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Employee
    template_name = 'user_list.html'

class FoodDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Food
    template_name = 'food_detail.html'
    permission_required = 'webapp.view_food'


class FoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Food
    template_name = 'food_create.html'
    form_class = FoodForm
    permission_required = 'webapp.add_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})

class FoodListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Food
    template_name = 'food_list.html'
    permission_required = 'webapp.view_food'

class FoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Food
    template_name = 'food_update.html'
    form_class = FoodForm
    permission_required = 'webapp.change_food'

    def get_success_url(self):
        return reverse('webapp:food_detail', kwargs={'pk': self.object.pk})

class FoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Food
    template_name = 'food_delete.html'
    permission_required = 'webapp.delete_food'

    def get_success_url(self):
        return reverse ('webapp:food_list')


class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    permission_required = 'webapp.view_order'

class OrderCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Order
    template_name = 'order_create.html'
    form_class = OrderForm
    permission_required = 'webapp.add_order'

    def form_valid(self, form):
        form.instance.operator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})

class OrderDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    permission_required = 'webapp.view_order'

class OrderCancelView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Order
    template_name = 'order_cancel.html'
    permission_required = 'webapp.delete_order'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'order_cancel.html', {'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = 'canceled'
        order.save()
        return redirect('webapp:order_list')

class OrderUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderForm
    permission_required = 'webapp.change_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


# классовое на базе View
class OrderDeliverView(LoginRequiredMixin, PermissionRequiredMixin, View):
    model = Order
    # template_name = 'order_deliver.html'
    permission_required = 'webapp.change_order_status'

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if order.status == 'preparing':
            order.courier = request.user
            order.status = 'on_way'
        elif (order.status == 'on_way') and (order.courier == request.user):
            order.status = 'delivered'
        order.save()
        return redirect('webapp:order_list')



class OrderFoodCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_create.html'
    permission_required = 'webapp.add_orderfood'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})

class OrderFoodUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = OrderFood
    form_class = OrderFoodForm
    template_name = 'order_food_update.html'
    permission_required = 'webapp.change_orderfood'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_food'] = OrderFood.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order_food = OrderFood.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})


class OrderFoodDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = OrderFood
    template_name = 'order_food_delete.html'
    permission_required = 'webapp.delete_orderfood'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_food'] = OrderFood.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.order_food = OrderFood.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})
