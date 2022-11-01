from django.contrib import admin

# Register your models here.
from personal_area.models import Appeal, Applicant, Address, Deputy, ConsiderationStage, Decision, BenefitCategory, \
    Constituency, AppealCategory, Message, Sender, Topic, SocialStatus


admin.site.register(Appeal)
admin.site.register(AppealCategory)
admin.site.register(Constituency)
admin.site.register(BenefitCategory)
admin.site.register(Decision)
admin.site.register(ConsiderationStage)
admin.site.register(Deputy)
admin.site.register(Address)
admin.site.register(Applicant)
admin.site.register(Message)
admin.site.register(Sender)
admin.site.register(Topic)
admin.site.register(SocialStatus)

