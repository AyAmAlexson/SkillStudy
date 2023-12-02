from .models import ResProperties, Comments, Viewings, Contracts, Clients, Owners, Agents, Features
from modeltranslation.translator import register, \
    TranslationOptions  # импортируем декоратор для перевода и класс настроек, от которого будем наследоваться


# регистрируем наши модели для перевода

@register(ResProperties)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'ref', 'prop_division', 'prop_type', 'location', 'address', '_price', 'status', 'status_valid', 'off_the_market',
        'bedrooms', 'bathrooms', 'prop_description', 'date_added', 'date_added', 'date_expected',
        'time_updated', 'owner', 'added_by', 'lf')



@register(Comments)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('re_property', 'added_by', 'comment', 'added_on')


@register(Viewings)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('re_property', 'client', 'agent', 'date')


@register(Contracts)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('re_property', 'client', 'agent', 'move_in_date', 'sign_date', 'period', 'final_price', 'af_paid',
              'deposit_paid', 'contract_signed')


@register(Clients)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('first_name','last_name','phone_1','phone_2','phone_3','email','added_by','date_added')


@register(Owners)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('activated', 'first_name', 'last_name', 'phone_1', 'phone_2', 'phone_3', 'email', 'added_by', 'date_added')


@register(Agents)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('contracts_closed', 'revenue_generated')


@register(Features)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('prop_feature',)
