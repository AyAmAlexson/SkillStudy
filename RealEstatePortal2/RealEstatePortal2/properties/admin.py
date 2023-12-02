from django.contrib import admin
from .models import ResProperties, Comments, Viewings, Contracts, Clients, Owners, Agents, Features
from modeltranslation.admin import \
    TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class ResPropertiesAdmin(TranslationAdmin):
    model = ResProperties


class CommentsAdmin(TranslationAdmin):
    model = Comments

class ViewingsAdmin(TranslationAdmin):
    model = Viewings

class ContractsAdmin(TranslationAdmin):
    model = Contracts


class ClientsAdmin(TranslationAdmin):
    model = Clients

class OwnersAdmin(TranslationAdmin):
    model = Owners

class AgentsAdmin(TranslationAdmin):
    model = Agents


class FeaturesAdmin(TranslationAdmin):
    model = Features


admin.site.register(ResProperties)
admin.site.register(Comments)
admin.site.register(Viewings)
admin.site.register(Contracts)
admin.site.register(Clients)
admin.site.register(Owners)
admin.site.register(Agents)
admin.site.register(Features)

