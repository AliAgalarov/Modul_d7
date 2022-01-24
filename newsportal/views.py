from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from .models import Author, Category, Post, Comment
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.template.loader import render_to_string

from .filters import NewsFilter
from .forms import NewsForm
from .models import Post, Category

from .tasks import send_mail_for_sub_once

class NewsList(ListView):
    model = Post
    template_name = 'newsPort_list.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context





class NewsDetailView(DetailView):
    template_name = 'newsPort_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # общаемся к содержимому контекста нашего представления
        id = self.kwargs.get('pk')  # получаем ИД поста (выдергиваем из нашего объекта из модели Пост)
        # формируем запрос, на выходе получим список имен пользователей subscribers__username, которые находятся
        # в подписчиках данной группы, либо не находятся
        qwe = Category.objects.filter(pk=Post.objects.get(pk=id).category.id).values("subscribers__username")
        # Добавляем новую контекстную переменную на нашу страницу, выдает либо правду, либо ложь, в зависимости от
        # нахождения нашего пользователя в группе подписчиков subscribers
        context['is_not_subscribe'] = not qwe.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = qwe.filter(subscribers__username=self.request.user).exists()
        return context



class NewsAddView(CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    success_url = '/news/'



class NewsEditView(UpdateView):
    template_name = 'newsP_edit.html'
    form_class = NewsForm
    success_url = '/news/'


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class NewsDeleteView(DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


# функция отписки от группы
@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')



class AddNews(PermissionRequiredMixin, NewsAddView):
    permission_required = ('newsportal.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsEditView):
    permission_required = ('newsportal.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDeleteView):
    permission_required = ('newsportal.delete_post',)


def send_mail_for_sub(instance):
    print('Представления - начало')
    print()
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')

    sub_text = instance.text
    # получаем нужный объект модели Категория через рк Пост
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    # для удобства вывода инфы в консоль, никакой важной функции не несет
    print('Адреса рассылки:')
    for qaz in subscribers:
        print(qaz.email)

    print()
    print()
    print()
    for subscriber in subscribers:
        # для удобства вывода инфы в консоль, никакой важной функции не несет
        print('**********************', subscriber.email, '**********************')
        print(subscriber)
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': instance})

        sub_username = subscriber.username
        sub_useremail = subscriber.email


        print()
        print(html_content)
        print()


        send_mail_for_sub_once.delay(sub_username, sub_useremail, html_content)





    print('Представления - конец')

    return redirect('/news/')