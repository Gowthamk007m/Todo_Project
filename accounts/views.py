
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView,FormView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from accounts.models import Task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



# Create your views here.

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'i'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context['i']=context['i'].filter(user=self.request.user)
        context['count']=context['i'].filter(complete=False).count()

        search_input=self.request.GET.get('search_area') or ''
        if search_input:
            context['i']= context['i'].filter(title__icontains=search_input)

        context['search_input']=search_input

        return context




class TaskDetails(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'i'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'create.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'create.html'
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate,self).form_valid(form)

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = "i"
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks')

class CustomLogin(LoginView):
    template_name = 'login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register,self).form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register ,self).get(*args,**kwargs)