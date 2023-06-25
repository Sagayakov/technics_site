from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.views.generic.base import View

from .models import Technics, Mark
from .forms import CommentForm


class CategoryView:
    def get_mark(self):
        return Mark.objects.all()

    def get_year(self):
        return Technics.objects.filter(is_public=True).values('year')


class TechnicsView(CategoryView, ListView):
    """Список всей техники"""

    model = Technics
    queryset = Technics.objects.filter(is_public=True)
    template_name = 'technics/technics.html'


class TechnicDetailView(CategoryView, DetailView):
    """Один экземпляр техники"""

    model = Technics
    slug_field = 'slug'
    template_name = 'technics/technics_detail.html'
    context_object_name = 'technic'


class AddCommentsView(View):
    """Отзывы"""

    def post(self, request, pk):
        form = CommentForm(request.POST)
        technic = Technics.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)

            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))

            form.technic = technic
            form.save()
        return redirect(technic.get_absolute_url())


class FilterTechView(CategoryView, ListView):
    """Фильтр техники"""

    template_name = 'technics/technics.html'

    def get_queryset(self):
        queryset = Technics.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(mark__in=self.request.GET.getlist('mark')) |
            Q(category__in=self.request.GET.getlist('category'))
        )
        return queryset
