from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from .models import InventoryItem
from django.contrib.auth.mixins import LoginRequiredMixin

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