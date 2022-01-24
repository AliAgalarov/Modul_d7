from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from .models import Product
from django.shortcuts import render
from django.views import View  # импортируем простую вьюшку
from django.core.paginator import Paginator




class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'



# создаём представление, в котором будут детали конкретного отдельного товара
class ProductDetail(DetailView):
    model = Product  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'product.html'  # название шаблона будет product.html
    context_object_name = 'product'


class Products(View):

    def get(self, request):
        products = Product.objects.order_by('-price')
        p = Paginator(products, 1)
        products = p.get_page(request.GET.get('page', 1))

        data = {
            'products': products,
        }
        return render(request, 'product_list.html', data)


class Products(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 1









