from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView
from .forms import UserRegisterForm, InventoryItemForm, CategoryForm
from django.contrib.auth import authenticate, login
from .models import InventoryItem, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
class Index(TemplateView):
	template_name = 'inventory/index.html'

class Inventory(LoginRequiredMixin, View):
	def get(self, request):
		items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

		return render(request, 'inventory/inventory.html', {'items': items})

class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'inventory/dashboard.html')

class Finance(LoginRequiredMixin, View):
	def get(self, request):
		return render(request, 'inventory/finance.html')

class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', { 'form': form })

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')
		
		return render(request, 'inventory/signup.html', {'form': form})
	
class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('inventory')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
	
class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('inventory')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete-item.html'
	success_url = reverse_lazy('inventory')
	context_object_name = 'item'

class ManageCategory(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'inventory/manage-category.html'
	context_object_name = 'categories'

class AddCategory(LoginRequiredMixin, CreateView):
	model = Category
	form_class = CategoryForm
	template_name = 'inventory/category-form.html'
	success_url = reverse_lazy('manage-category')

class EditCategory(LoginRequiredMixin, UpdateView):
	model = Category
	form_class = CategoryForm
	template_name = 'inventory/category-form.html'
	success_url = reverse_lazy('manage-category')

class DeleteCategory(LoginRequiredMixin, DeleteView):
	model = Category
	template_name = 'inventory/category-delete.html'
	success_url = reverse_lazy('manage-category')