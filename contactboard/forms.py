from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Classe, Curs, validate_valid_id, telfRegex

def validate_classe_id_unique(value):
    if Classe.objects.filter(id_interna=value).exists():
        raise ValidationError('%(value)s already exists',
            params={'value': value})

def validate_curs_id_unique(value):
    if Curs.objects.filter(id_interna=value).exists():
        raise ValidationError('%(value)s already exists',
            params={'value': value})

class ClasseForms:
    class NewForm(forms.Form):
        nom = forms.CharField(max_length=50, required=True)
        id_interna = forms.SlugField(max_length=20, required=True,
            validators=[validate_valid_id, validate_classe_id_unique],
            help_text='Forma curta de referir-se a la classe. Ha de ser única i'
            ' <em>no</em> es pot canviar més endavant.')
        curs = forms.CharField(disabled=True, required=False)

    class EditForm(NewForm):
        id_interna = forms.SlugField(disabled=True, required=False)
        curs = forms.ModelChoiceField(queryset=Curs.objects.all(),
            required=True, to_field_name='id_interna', empty_label=None)

class CursForms:
    class NewForm(forms.Form):
        nom = forms.CharField(max_length=50, required=True)
        id_interna = forms.SlugField(max_length=20, required=True,
            validators=[validate_curs_id_unique],
            help_text='Forma curta de referir-se al curs. Ha de ser única i'
            ' <em>no</em> es pot canviar més endavant.')
        ordre = forms.IntegerField(required=False, min_value=0, max_value=32767,
            help_text='Ordre dels cursos. Ex.: 1er ESO = 1, 2on ESO = 2, ...,'
            ' 1er Batx = 5...')
    class EditForm(forms.Form):
        nom = forms.CharField(max_length=50, required=True)
        id_interna = forms.SlugField(disabled=True, required=False)
        ordre = forms.IntegerField(required=False, min_value=0, max_value=32767,
            help_text='Ordre dels cursos. Ex.: 1er ESO = 1, 2on ESO = 2, ...,'
            ' 1er Batx = 5...')

class AlumneForms:
    class NewForm(forms.Form):
        nom = forms.CharField(max_length=255, required=True)
        cognoms = forms.CharField(max_length=255, required=True)
        classe = forms.CharField(disabled=True, required=False)
        data_de_naixement = forms.DateField(required=True, input_formats=[
            '%Y-%m-%d',  # ISO
            '%d-%m-%Y',
            '%d/%m/%Y',
            '%d-%m-%y',
            '%d/%m/%y'
        ])
        correu_alumne = forms.EmailField(required=False)
        correu_pare = forms.EmailField(required=False)
        telefon_pare = forms.CharField(required=False, max_length=15,
            validators=[RegexValidator(telfRegex)],
            label='Telèfon pare')
        correu_mare = forms.EmailField(required=False)
        telefon_mare = forms.CharField(required=False, max_length=15,
            validators=[RegexValidator(telfRegex)],
            label='Telèfon mare')
        compartir = forms.BooleanField(required=False, initial=False,
            help_text='Si es selecciona, la classe podrà veure els correus i'
            ' els telèfons')

    class EditForm(NewForm):
        classe = forms.ModelChoiceField(required=True,
            to_field_name='id_interna',
            queryset=Classe.objects.all().order_by('curs'))

class MailtoForm(forms.Form):
    TO_ALUMNES = 'alumnes'
    TO_PARES = 'pares'
    TO_MARES = 'mares'
    TO = [
        (TO_ALUMNES, 'Alumnes'),
        (TO_PARES, 'Pares'),
        (TO_MARES, 'Mares')
    ]
    enviar_a = forms.MultipleChoiceField(choices=TO,
        widget=forms.CheckboxSelectMultiple)
    no_cco = forms.BooleanField(required=False, help_text='Per privacitat, '
        "els correus s'envien amb còpia oculta. Marqui aixó per enviar com "
        'destinataris directes ("Per a"). Aixó permet que tothom vegi les '
        'adresses')
    #from django.db.utils import OperationalError

    def __init__(self, *args, **kwargs):
        super(MailtoForm, self).__init__(*args, **kwargs)
        self.fields['classes'] = forms.MultipleChoiceField(choices=[
            (classe.id_interna, str(classe))
            for classe in Classe.objects.all()])

class MailtoClasseForm(MailtoForm):
    classes = None