# from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from personal_area.models import *
# from .models import Form_for_Appeal
# from django.core.mail import send_mail, BadHeaderError
from datetime import datetime
from django.shortcuts import redirect, render,HttpResponse
from random import randint
from .forms import Appeal_form, Search_form, Search_appeals_form
from django.urls import reverse
# @csrf_protect


def success(request):
    return HttpResponse("appeals/success.html")
    # print("долбаеб ")
    
def send_appeal(request):
    number=11111
    pin=11111
    if request.method == 'POST':
        form = Appeal_form(request.POST)
        print('Ну данные я получил и дальше что')
        if form.is_valid():
            # необходимо поменять присвоение переменной уникального номера
            # и добавить pin и номер обращения в БД
            
            pin=randint(1000,9999)
            plus=randint(100,999)
            pin=pin+plus
            if pin>9999:
                pin=pin-randint(100,999)
            
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            patronymic = form.cleaned_data['patronymic']
            email = form.cleaned_data['email']
            phone= form.cleaned_data['phone']


            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            house = form.cleaned_data['house']


            type_of_appeal= form.cleaned_data['type_of_appeal']
            theme = form.cleaned_data['theme']
            category_of_benefits = form.cleaned_data['category_of_benefits']
            social_situation = form.cleaned_data['social_situation']
            deputy = form.cleaned_data['deputy'].split(' ')

            message = form.cleaned_data['message']
            date_of_ordering=datetime.now()

            body = {'name': name,
            'surname':surname ,
            'patronymic':patronymic ,
            'city':city ,
            'street':street ,
            'house': house,
            'email':email ,
            'phone': phone,
            'type_of_appeal':type_of_appeal,
            'theme':theme ,
            'category_of_benefits':category_of_benefits ,
            'social_situation':social_situation ,
            'deputy': deputy,
            'message': message,
            'date_of_ordering':date_of_ordering ,
            }
            print(body)

            address=Address(city="Реж",street=street,house=house)
            benefit=BenefitCategory.objects.get(name=category_of_benefits)
            type_of_appeal=AppealCategory.objects.get(name=type_of_appeal)
            consideration_stage=ConsiderationStage.objects.get(name='Поступило')
            deputy=Deputy.objects.get(pk=1)
            social_status = SocialStatus.objects.get(name=social_situation)
            topic = Topic.objects.get(name=theme)
            applicant=Applicant(social_status=social_status, name=name,surname=surname,patronymic=patronymic,address=address, benefit=benefit,email=email,phone=phone)
            decision=Decision.objects.get(name='Не рассмотрено')
            content = message
            appeal=Appeal(pin=pin, topic=topic, time_create=date_of_ordering,category=type_of_appeal,applicant=applicant,responsible_person=deputy,consideration_stage=consideration_stage,decision=decision, content=content)
            sender = Sender.objects.get(pk=2)
            message_text=Message(content=message,appeal=appeal,sender=sender,applicant=applicant,deputy=deputy)
            address.save()
            applicant.save()
            appeal.save()
            message_text.save()
            try:
                number=Appeal.objects.get(pk=number)
            except:
                print('нюхай бебру')
            request.session['form_is_correct_key'] = 97231 * int(appeal.pk) + 68963 * int(appeal.pin)
            request.session.set_expiry(900)
            context = {'appeal': appeal, 'messages': [], 'is_deputy': False}
            return redirect('redirect_form', appeal.pk)
        else:
            print(form.is_valid(),'\nОшибки:',form.errors)
        # success(request,number,pin)
        # return redirect("success")
    
    form = Appeal_form()

    return render(request, "appeals_final/Форма-для-обращения.html", {'form': form,'number':number,'pin':pin})


def review_appeals(request, appeal_id):
    appeal = Appeal.objects.get(pk=appeal_id)
    sender = Sender.objects.get(sender='deputy')
    answers = Message.objects.filter(appeal=appeal, sender=sender)
    time = None
    if appeal.decision_time:
        time = (appeal.decision_time - appeal.time_create).days
    answer = None
    if len(answers) != 0:
        answer = answers[len(answers) - 1]
    return render(request, 'appeals_final/Просмотр-обращения-на-обзоре.html', {'appeal': appeal, 'answer': answer, 'time': time})


def review_appeal_peoples(request):
    appeals = Appeal.objects.all()
    topic = None
    category = None
    number = None
    print(request.POST)
    if request.POST:
        form = Search_appeals_form(request.POST)
        if form.is_valid():
            pass
        if 'number' in form.cleaned_data:
            number = form.cleaned_data['number']
        try:
            topic = Topic.objects.get(name=form.cleaned_data['topic'])
        except:
            pass
        try:
            category = AppealCategory.objects.get(name=form.cleaned_data['category'])
        except:
            pass
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        if str(number).isdigit():
            try:
                appeals = [Appeal.objects.get(pk=number, time_create__gte=start_time, time_create__lte=end_time)]
            except:
                pass
        else:
            if topic is None and category is not None:
                appeals = Appeal.objects.filter(category=category, time_create__gte=start_time,
                                                 time_create__lte=end_time)
            elif topic is not None and category is None:
                appeals = Appeal.objects.filter(topic=topic, time_create__gte=start_time, time_create__lte=end_time)
            elif topic is None and category is None:
                appeals = Appeal.objects.filter(time_create__gte=start_time, time_create__lte=end_time)
            else:
                appeals = Appeal.objects.filter(category=category, topic=topic, time_create__gte=start_time, time_create__lte=end_time)

    print(appeals)
    return render(request, 'appeals_final/Обзор-обращений-граждан.html', {'appeals': appeals})


def redirect_form(request, appeal_id):
    appeal = Appeal.objects.get(pk=appeal_id)
    return render(request, 'appeals_final/Форма-перенаправление.html', {'appeal': appeal})
