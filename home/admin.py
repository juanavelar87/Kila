from django import forms
from django.contrib import admin
from .models import Usuario
from .models import Obra
from .models import Semana
from .models import Valor_Indicador
from .models import Documento
from .models import Indicadores

admin.site.register(Obra)
admin.site.register(Valor_Indicador)
admin.site.register(Documento)
admin.site.register(Indicadores)

class YourModelForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def save(self, commit=True):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2 or password1 != password2:
            return super(YourModelForm, self).save(commit=commit)
        user = super(YourModelForm, self).save(commit=False)
        user.set_password(password1)
        return super(YourModelForm, self).save(commit=commit)

    def __init__(self, *args, **kwargs):
        super(YourModelForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
    
    class Meta:
        model = Usuario
        fields = '__all__'

class YourModelAdmin(admin.ModelAdmin):
    form = YourModelForm
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email','is_superuser','is_active', 'is_staff','password1', 'password2'),
        }),
    )
admin.site.register(Usuario, YourModelAdmin)

class YModelAdmin(admin.ModelAdmin):
    form = YourModelForm
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email','is_superuser','is_active', 'is_staff','password1', 'password2'),
        }),
    )
admin.site.register(Semana)
