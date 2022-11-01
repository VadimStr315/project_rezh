import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from personal_area.models import *
import personal_area


def deputy_commission(request):
    return render(request, 'main_final/Депутатские-комиссии.html')


def municipal_service(request):
    return render(request, 'main_final/Муниципальная-служба.html')


def index(request):
    return render(request, 'main_final/Главная.html')


def news(request):
    return render(request, 'main_final/Новости.html')


class News(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'main_final/Новости.html'


def news_detail(request):
    return render(request, 'main_final/Новость-12-05-22.html')


def about(request):
    return render(request, 'main_final/О-Думе.html')


def vote(request):
    return render(request, 'main_final/Голосование.html')


def access_check(request, appeal_id):
    appeal = Appeal.objects.get(pk=appeal_id)
    if 'form_is_correct_key' in request.session:
        return request.session['form_is_correct_key'] == 97231 * int(appeal.pk) + 68963 * int(appeal.pin)
    return False


class ShowDetailAppealToApplicant(UserPassesTestMixin, DetailView):
    model = Appeal
    context_object_name = 'appeal'
    template_name = 'personal_area_final/Данные-по-обращению.html'
    pk_url_kwarg = 'appeal_id'

    def test_func(self):
        appeal = Appeal.objects.get(pk=self.kwargs['appeal_id'])
        return self.request.session['form_is_correct_key'] == 97231 * int(appeal.pk) + 68963 * int(appeal.pin)


def show_appeal_to_applicant(request, appeal_id):
    if not access_check(request, appeal_id):
        return redirect('appeals_info')

    is_deputy = False
    applicant = Appeal.objects.get(id=appeal_id).applicant
    appeal = Appeal.objects.get(pk=appeal_id)
    deputy = Deputy.objects.get(pk=appeal.responsible_person.pk)
    sender = Sender.objects.get(pk=2)

    print(request.POST)
    if 'message' in dict(request.POST).keys() and request.POST['message']:
        msg = Message(content=request.POST['message'], appeal=appeal, deputy=deputy, sender=sender, applicant=applicant)
        msg.save()

    messages = Message.objects.filter(appeal=appeal, deputy=deputy, applicant=applicant)
    context = {'appeal': appeal, 'messages': messages, 'is_deputy': is_deputy}
    return render(request, 'personal_area_final/Обращение-(001).html', context=context)


def appeals_info(request):
    if 'pincode' in request.POST and 'number' in request.POST:
        appeal_id = request.POST['number']
        pin = request.POST['pincode']
        appeal = None
        try:
            appeal = Appeal.objects.get(pk=appeal_id)
        except:
            pass

        if appeal is not None:
            if str(appeal.pin) == str(pin):
                request.session['form_is_correct_key'] = 97231 * int(appeal.pk) + 68963 * int(appeal.pin)
                request.session.set_expiry(900)
                return redirect('my_appeal', appeal_id=appeal_id)

    return render(request, 'appeals_final/Обращения.html')
    
