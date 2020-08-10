from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.conf import settings

from core.services import image_created, resized_image_as_str
from core.forms import AddImageForm, ResizeImageForm
from core.models import Image


class HomePageView(ListView):
    model = Image
    template_name = 'core/home_page.html'
    paginate_by = settings.ITEMS_ON_HOME_PAGE


class AddImageView(View):
    def get(self, request):
        add_image_form = AddImageForm
        context = {'add_image_form': add_image_form}
        return render(request, 'core/add_image_page.html', context)

    def post(self, request):
        add_image_form = AddImageForm(request.POST, request.FILES)
        context = {'add_image_form': add_image_form, 'errors': add_image_form.errors}
        if add_image_form.is_valid():
            slug = get_random_string()
            if image_created(add_image_form, slug):
                return redirect('image-detail-page', slug=slug)

            add_image_form.errors['url'] = ['Не удалось загрузить изображение']
        return render(request, 'core/add_image_page.html', context)


class ImageDetailView(FormMixin, DetailView):
    model = Image
    template_name = 'core/image_detail_page.html'
    form_class = ResizeImageForm

    def get_context_data(self, **kwargs):
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        context['form'] = ResizeImageForm
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        resize_image_form = ResizeImageForm(request.POST)
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        if resize_image_form.is_valid():
            context['resized_image'] = resized_image_as_str(self.object, resize_image_form)
            return render(request, 'core/image_detail_page.html', context)

        context['errors'] = resize_image_form.errors
        return render(request, 'core/image_detail_page.html', context)
