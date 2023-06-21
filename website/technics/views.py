from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.views.generic.base import View

from .models import Technics
from .forms import CommentForm


class TechnicsView(ListView):
    """Список всей техники"""

    model = Technics
    queryset = Technics.objects.filter(is_public=True)
    template_name = 'technics/technics.html'
    # context_object_name = 'technics'


class TechnicDetailView(DetailView):
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
