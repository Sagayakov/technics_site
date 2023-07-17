from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Technics, Mark, UserTechRelation
from .forms import CommentForm
from .serializers import TechSerializer, UserTechRelationSerializer
from .permissions import IsOwnerOrAdminOrReadOnly


class CategoryView:
    """Достает объекты модели"""

    def get_mark(self):
        return Mark.objects.all().order_by('mark')

    def get_year(self):
        return Technics.objects.filter(is_public=True).values('year').order_by('year').distinct()


class TechnicsView(CategoryView, ListView):
    """Список всей техники"""

    model = Technics
    queryset = Technics.objects.filter(is_public=True).order_by('-price')
    template_name = 'technics/technics.html'
    paginate_by = 9


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
    paginate_by = 6

    def get_queryset(self):
        queryset = Technics.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(mark__in=self.request.GET.getlist('mark')) |
            Q(category__in=self.request.GET.getlist('category'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['mark'] = ''.join([f'mark={x}&' for x in self.request.GET.getlist('mark')])
        context['category'] = ''.join([f'category={x}&' for x in self.request.GET.getlist('category')])
        return context


class Search(ListView):
    """Поиск техники"""

    template_name = 'technics/technics.html'
    paginate_by = 6

    def get_queryset(self):
        return Technics.objects.filter(model__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        return context


class TechViewSet(ModelViewSet):
    """API Technics"""

    queryset = Technics.objects.all()
    serializer_class = TechSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filterset_fields = ['price']
    search_fields = ['description', 'small_description']
    ordering_fields = ['price', 'model', 'category']

    def perform_create(self, serializer):
        """Добавление юзера-создателя в объект модели Technics"""

        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserTechRelationView(UpdateModelMixin, GenericViewSet):
    """API UserTechRelation"""

    permission_classes = [IsAuthenticated]
    queryset = UserTechRelation.objects.all()
    serializer_class = UserTechRelationSerializer
    lookup_field = 'tech'

    def get_object(self):
        obj, _ = UserTechRelation.objects.get_or_create(user=self.request.user,
                                                        technics_id=self.kwargs['tech'])
        return obj
