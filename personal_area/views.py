import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .forms import LoginUserForm, FindAppealsForm
from .models import Appeal, Deputy, Message, Sender, Decision, ConsiderationStage, Topic, AppealCategory


def get_analytic_data():
    completed_percent = 0
    new_percent = 0
    average_decision_time = 0
    total_count = Appeal.objects.count()
    print(total_count)
    completed_count = Appeal.objects.filter(
        consideration_stage=ConsiderationStage.objects.get(name='Рассмотрено')).count()
    new_count = Appeal.objects.filter(
        consideration_stage=ConsiderationStage.objects.get(name='Поступило')).count()
    top_appeals_from_topics = Appeal.objects.values('topic').annotate(total=Count('id')).order_by('-total')[:5] #
    # Передать в словарь "Топ 5 тем обращений"
    for e in top_appeals_from_topics:
        e['topic'] = Topic.objects.get(pk=e['topic']).name
        e['percent'] = int(int(e['total']) / total_count * 100)

    completed_appeals = Appeal.objects.exclude(decision_time__isnull=True)
    completed_appeals_count = completed_appeals.count()

    summ = 0
    for appeal in completed_appeals:
        summ += (appeal.decision_time - appeal.time_create).days
    if total_count != 0:
        completed_percent = int(completed_appeals_count/total_count*100)
        new_percent = int(new_count/total_count*100)

    if completed_appeals_count != 0:
        average_decision_time = summ//completed_appeals_count # Среднее время обращения
    analytic_data = {
        'total': total_count,
        'completed_percent': completed_percent,
        'new_percent': new_percent,
        'completed': completed_count,
        'new': new_count,
        'top_appeals_from_topics': top_appeals_from_topics,
        'top_appeals_from_topics_count': len(top_appeals_from_topics),
        'average_decision_time': average_decision_time
    }
    return analytic_data


class AppealHome(LoginRequiredMixin, ListView):
    model = Appeal
    context_object_name = 'appeals'
    template_name = 'personal_area_final/Профиль.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        deputy = Deputy.objects.get(user_id=self.request.user.id)
        deputy_id = deputy.id
        context['appeals'] = Appeal.objects.filter(responsible_person_id=deputy_id)
        context['deputy'] = deputy
        context['analytic_data'] = get_analytic_data()
        return context


def get_analytic_data_for_detail():
    completed_appeals = Appeal.objects.exclude(decision_time__isnull=True)
    completed_appeals_count = completed_appeals.count()
    summ = 0
    for appeal in completed_appeals:
        summ += (appeal.decision_time - appeal.time_create).days
    average_decision_time = summ // completed_appeals_count  # Среднее время обращения
    total_count = Appeal.objects.count()
    appeals_from_category = Appeal.objects.values('category').annotate(total=Count('id')).order_by('id')
    for el in appeals_from_category:
        el['category'] = AppealCategory.objects.get(pk=el['category']).name
    appeals_from_decision = Appeal.objects.values('decision').annotate(total=Count('id')).order_by('id')
    for el in appeals_from_decision:
        el['decision'] = Decision.objects.get(pk=el['decision']).name
    appeals_from_topic = Appeal.objects.values('topic').annotate(total=Count('id')).order_by('id')
    for el in appeals_from_topic:
        el['topic'] = Topic.objects.get(pk=el['topic']).name
        el['percent'] = round(int(el['total']) / total_count * 100, 1)
    analytic_data = {
        'total': total_count,
        'average_decision_time': average_decision_time,
        'appeals_from_category': appeals_from_category,
        'appeals_form_decision': appeals_from_decision,
        'appeals_from_topic': appeals_from_topic
    }
    return analytic_data


def analytic_detail(request):
    appeals_for_topic = Appeal.objects.values('topic').annotate(total=Count('id')).order_by('total')
    appeals_for_categories = Appeal.objects.values('category').annotate(total=Count('id'))
    analytic_data = get_analytic_data_for_detail()
    form = FindAppealsForm
    print(analytic_data)

    if request.POST:
        pass

    return render(request, 'personal_area_final/Подробная-аналитика.html', {'analytic_data': analytic_data, 'form': form})


def user_check(user, appeal_id):
    deputy_id = Deputy.objects.get(user_id=user.id).id
    responsible_p_id = Appeal.objects.get(id=appeal_id).responsible_person_id
    return deputy_id == responsible_p_id


@login_required(redirect_field_name='personal_area')
def show_appeal_to_deputy(request, appeal_id):
    global message_decision
    if not user_check(request.user, appeal_id):
        return redirect('personal_area')

    is_deputy = True
    applicant = Appeal.objects.get(id=appeal_id).applicant
    appeal = Appeal.objects.get(pk=appeal_id)
    deputy = Deputy.objects.get(user=request.user)
    sender = Sender.objects.get(pk=1)

    print('GET ЗАПРОС - ', end='')
    print(request.GET)

    if 'approved' in request.POST:
        appeal.decision = Decision.objects.get(name='Одобрено')
        appeal.decision_time = datetime.datetime.now()
        appeal.consideration_stage = ConsiderationStage.objects.get(name='Рассмотрено')
        message_decision = Message(content='Ваше решение было одобрено.', appeal=appeal, deputy=deputy, sender=sender,
                          applicant=applicant)
        appeal.save()
        message_decision.save()
    elif 'denied' in request.POST:
        appeal.decision = Decision.objects.get(name='Отказано')
        appeal.decision_time = datetime.datetime.now()
        appeal.consideration_stage = ConsiderationStage.objects.get(name='Рассмотрено')
        message_decision = Message(content='По вашему решению было решено отказать.', appeal=appeal, deputy=deputy, sender=sender,
                          applicant=applicant)
        appeal.save()
        message_decision.save()
    elif 'redirect' in request.POST:
        appeal.decision = Decision.objects.get(name='Перенаправлено')
        appeal.decision_time = datetime.datetime.now()
        appeal.consideration_stage = ConsiderationStage.objects.get(name='Рассмотрено')
        message_decision = Message(content='Ваше обращение будет перенаправлено.', appeal=appeal, deputy=deputy, sender=sender,
                          applicant=applicant)
        appeal.save()
        message_decision.save()
    elif 'clarified' in request.POST:
        appeal.decision = Decision.objects.get(name='Разъяснено')
        appeal.decision_time = datetime.datetime.now()
        appeal.consideration_stage = ConsiderationStage.objects.get(name='Рассмотрено')
        message_decision = Message(content='Информация по обращению разъяснена.', appeal=appeal, deputy=deputy, sender=sender,
                          applicant=applicant)
        appeal.save()
        message_decision.save()


    print(request.POST)
    if 'message' in dict(request.POST).keys() and request.POST['message']:
        msg = Message(content=request.POST['message'], appeal=appeal, deputy=deputy, sender=sender, applicant=applicant)
        msg.save()

    messages = Message.objects.filter(appeal=appeal, deputy=deputy, applicant=applicant)
    context = {'appeal': appeal, 'messages': messages, 'is_deputy': is_deputy}
    return render(request, 'personal_area_final/Обращение-(001).html', context=context)


class ShowDetailAppeal(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Appeal
    context_object_name = 'appeal'
    template_name = 'personal_area_final/Данные-по-обращению.html'
    pk_url_kwarg = 'appeal_id'

    def test_func(self):
        deputy_id = Deputy.objects.get(user_id=self.request.user.id).id
        responsible_p_id = Appeal.objects.get(id=self.kwargs['appeal_id']).responsible_person_id
        return deputy_id == responsible_p_id


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'personal_area_final/Авторизация.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admin:index')
        return reverse_lazy('personal_area')


def logout_user(request):
    logout(request)
    return redirect('auth')