from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.shortcuts import render, get_object_or_404

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

@login_required
def birthday(request):
    # Если есть параметры POST-запроса...
    if request.POST:
        # ...передаем параметры запроса в конструктор класса формы
        form = BirthdayForm(request.POST)
        # context = {'form': form}
        
        # Если данные в форме валидны
        if form.is_valid():
            # form.save()
            instance = form.save(commit=False)
            instance.author = request.user # Назначаем автора
            instance.save() # Теперь сохраняем в БД
            # то считаем сколько дней осталось
            birthday_countdown = calculate_birthday_countdown(
                form.cleaned_data['birthday']
            )
            context = {
                'form': form,
                'birthday_countdown': birthday_countdown,
            }
            return render(request, 'birthday/birthday.html', context)
    # Если нет параметров POST-запроса, создаем пустую форму
    else:
        form = BirthdayForm()

    # Передаем форму в словарь контекста и возвращаем ответ
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context)


# def birthday_list(request):
#     # Получаем все объекты модели Birthday из БД.
#     birthdays = Birthday.objects.all()
#     # Передаём их в контекст шаблона.
#     context = {'birthdays': birthdays}
#     return render(request, 'birthday/birthday_list.html', context)


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object =self.get_object()
        return object.author == self.request.user

class BirthdayMixin:
 model = Birthday
 success_url = reverse_lazy('birthday:list') 

class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for birthday in context['page_obj']:
            birthday.countdown = calculate_birthday_countdown(birthday.birthday)
        return context

class UserPassesTestMixin:
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user
    
class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    
class BirthdayCreateView(LoginRequiredMixin, CreateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    #Переодресация пользователя
    # success_url = reverse_lazy('birthday:list')

 

class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'
    # success_url = reverse_lazy('birthday:list')


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    model = Birthday
    # # template_name = 'birthday/birthday.html'
    success_url = reverse_lazy('birthday:list')
    

# context = super().get_context_data(**kwargs)
# context['birthday_countdown'] = calculate_birthday_countdown(...)
# context['birthday_countdown'] = calculate_birthday_countdown(self.object.birthday)

class BirthdayDetailView(DetailView):
    model = Birthday
    def get_context_data(self, **kwargs):
        #Получаем словарь контекста
        context = super().get_context_data(**kwargs)
        #Добовляем новый ключ
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Добовляем словарь объекта в контекст
            self.object.birthday
        )
        return context
    
# class BirthdayListView(ListView):
#     model = Birthday
#     queryset = Birthday.objects.prefetch_related('tags')
#     ordering = 'id'
#     paginate_by = 10