from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from .models import RestaurantLocation
from .forms import RestaurantCreateForm,RestaurantLocationCreateForm
@login_required()
def restaurant_create_view(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors=None
    if form.is_valid():
        if request.user.is_authenticated():
            instance=form.save(commit=False)
            instance.owner=request.user
            instance.save()
        #obj=RestaurantLocation.objects.create(
        #    name=form.cleaned_data.get('name'),
        #    location=form.cleaned_data.get('location'),
        #    category=form.cleaned_data.get('category')
        #)
            return HttpResponseRedirect("/restaurants/")
        else:
            return HttpResponseRedirect("/login/")
    if form.errors:
        errors=form.errors
    template_name="form.html"
    context={"form":form,"errors":errors}
    return render(request,template_name,context)


def home(request):
    return render(request,"home.html",)

def about(request):
    return render(request,"about.html",)

def contact(request):
    return render(request,"contact.html",)

class ContactView(View):
    def get(self, request, *args,**kwargs):
        return render(request,"contact.html",)
class ContactTemplateView(TemplateView):
    template_name='contact.html'

def restaurant_listview(request):
    query_set=RestaurantLocation.objects.all()
    context={
    "object_list": query_set
    }
    return render(request,"restaurant_list.html",context)

class RestaurantListView(LoginRequiredMixin,ListView):
    template_name='restaurant_list.html'
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)


class RestaurantDetailView(LoginRequiredMixin,DetailView):
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)
    template_name='restaurant_detail.html'
#    def get_context_data(self,*args,**kwargs):
#        print(self.kwargs)
#        context=super(RestaurantDetailView, self).get_context_data(*args,**kwargs)
#        print(context)
#        return context
#    def get_object(self,*args,**kwargs):
#        rest_id=self.kwargs.get('rest_id')
#        object=get_object_or_404(RestaurantLocation,id=rest_id)
#        return object

class RestaurantCreateView(LoginRequiredMixin,CreateView):
    form_class=RestaurantLocationCreateForm
    template_name="form.html"
    #login_url="/login/"
    #success_url="/restaurants/"
    def form_valid(self,form):
        instance=form.save(commit=False)
        instance.owner=self.request.user
        #instance.save()
        return super(RestaurantCreateView,self).form_valid(form)

class RestaurantDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class=RestaurantLocationCreateForm
    template_name="restaurant_detail_update.html"
    def get_queryset(self):
        return RestaurantLocation.objects.filter(owner=self.request.user)
    #login_url="/login/"
    #success_url="/restaurants/"
