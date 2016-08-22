from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from ampadb.support import is_admin
from django.contrib.auth.decorators import login_required, user_passes_test
from usermanager.models import Profile
from django.urls import reverse

from .models import Classe, Alumne
from .forms import *

@login_required
def list(request, id_classe):
    classe = get_object_or_404(Classe, id_interna=id_classe)
    context = {
        'classe': classe,
        'alumnes': Alumne.objects.filter(classe=classe),
    }
    return render(request, 'contactboard/list.html', context)

@login_required
@user_passes_test(is_admin)
def adminlist(request):
    cursos = Curs.objects.all().order_by('ordre')
    classes = Classe.objects.all().order_by('curs')
    context = {
        'cursos': cursos,
        'classes': classes
    }
    return render(request, 'contactboard/adminlist.html', context)

@login_required
@user_passes_test(is_admin)
def add_classe(request, id_curs):
    curs = get_object_or_404(Curs, id_interna=id_curs)
    if request.method == 'POST':
        form = ClasseForms.NewForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            #return HttpResponse(str(cdata))
            classe = Classe()
            classe.nom = cdata['nom']
            classe.id_interna = cdata['id_interna']
            classe.curs = curs
            classe.save()
            return redirect('contactboard:adminlist')
    else:
        form = ClasseForms.NewForm(initial={'curs': curs})
    context = {
        'form': form,
        'submitText': 'Crear'
    }
    return render(request, 'contactboard/add.html', context)

@login_required
@user_passes_test(is_admin)
def edit_classe(request, id_classe):
    classe = get_object_or_404(Classe, id_interna=id_classe)
    if request.method == 'POST':
        form = ClasseForms.EditForm(request.POST)
        if form.is_valid():
            if form.has_changed:
                cdata = form.cleaned_data
                classe.nom = cdata['nom']
                classe.curs = cdata['curs']
                classe.save()
            return redirect('contactboard:adminlist')
    else:
        c = {
            'nom': classe.nom,
            'id_interna': classe.id_interna,
            'curs': classe.curs.id_interna
        }
        form = ClasseForms.EditForm(c, initial=c)
    context = {
        'form': form,
        'submitText': 'Editar'
    }
    return render(request, 'contactboard/add.html', context)

@login_required
@user_passes_test(is_admin)
def delete_classe(request, id_classe):
    classe = get_object_or_404(Classe, id_interna=id_classe)
    if request.method == 'POST':
        classe.delete()
        return redirect('contactboard:adminlist')
    context = {
        'classe': classe
    }
    return render(request, 'contactboard/delete-classe.html', context)

@login_required
@user_passes_test(is_admin)
def add_curs(request):
    if request.method == "POST":
        form = CursForms.NewForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            curs = Curs()
            curs.nom = cdata['nom']
            curs.id_interna = cdata['id_interna']
            if cdata['ordre']:
                curs.ordre = cdata['ordre']
            curs.save()
            return redirect('contactboard:adminlist')
    else:
        form = CursForms.NewForm()
    context = {
        'form': form,
        'submitText': 'Crear'
    }
    return render(request, 'contactboard/add.html', context)

@login_required
@user_passes_test(is_admin)
def edit_curs(request, id_curs):
    curs = get_object_or_404(Curs, id_interna=id_curs)
    if request.method == 'POST':
        if form.is_valid():
            if form.has_changed:
                cdata = form.cleaned_data
                curs.nom = cdata['nom']
                curs.ordre = cdata['ordre']
            return redirect('contactboard:adminlist')
    else:
        c = {
            'nom': curs.nom,
            'id_interna': curs.id_interna,
            'ordre': curs.ordre
        }
        form = CursForms.EditForm(c, initial=c)
    context = {
        'form': form,
        'submitText': 'Editar'
    }
    return render(request, 'contactboard/add.html', context)

@login_required
@user_passes_test(is_admin)
def delete_curs(request, id_curs):
    curs = get_object_or_404(Curs, id_interna=id_curs)
    if request.method == 'POST':
        curs.delete()
        return redirect('contactboard:adminlist')
    context = {
        'curs': curs,
        'classes': Classe.objects.filter(curs=curs)
    }
    return render(request, 'contactboard/delete-curs.html', context)

@login_required
@user_passes_test(is_admin)
def add_alumne(request, id_classe):
    classe = get_object_or_404(Classe, id_interna=id_classe)
    if request.method == 'POST':
        form = AlumneForms.NewForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            alumne = Alumne()
            alumne.nom = cdata['nom']
            alumne.cognoms = cdata['cognoms']
            alumne.classe = classe
            alumne.data_de_naixement = cdata['data_de_naixement']
            alumne.correu_alumne = cdata['correu_alumne']
            alumne.correu_pare = cdata['correu_pare']
            alumne.correu_mare = cdata['correu_mare']
            alumne.telefon_pare = cdata['telefon_pare']
            alumne.telefon_mare = cdata['telefon_mare']
            alumne.compartir = cdata['compartir']
            alumne.save()
            return redirect('contactboard:list', id_classe)
    else:
        form = AlumneForms.NewForm(initial={'classe': classe})
    context = {
        'form': form,
        'submitText': 'Afegir'
    }
    return render(request, 'contactboard/add.html', context)


@login_required
def edit_alumne(request, alumne_pk):
    if not is_admin(request.user):
        p = Profile.objects.get(user=request.user)
        if p.alumne.pk != int(alumne_pk):
            #return redirect('/contactboard/edit/{}'.format(p.alumne.pk))
            return redirect('contactboard:edit-alumne', p.alumne.pk)
        ThisForm = AlumneForms.EditForm

    alumne = get_object_or_404(Alumne, pk=alumne_pk)
    if request.method == 'POST':
        if is_admin(request.user):
            form = AlumneForms.AdminEditForm(request.POST)
        else:
            form = AlumneForms.EditForm(request.POST)
        if form.is_valid():
            if form.has_changed():
                cdata = form.cleaned_data
                alumne.nom = cdata['nom']
                alumne.cognoms = cdata['cognoms']
                alumne.classe = cdata['classe']
                alumne.data_de_naixement = cdata['data_de_naixement']
                alumne.correu_alumne = cdata['correu_alumne']
                alumne.correu_pare = cdata['correu_pare']
                alumne.correu_mare = cdata['correu_mare']
                alumne.telefon_pare = cdata['telefon_pare']
                alumne.telefon_mare = cdata['telefon_mare']
                alumne.compartir = cdata['compartir']
                alumne.save()
            return redirect('contactboard:list', alumne.classe.id_interna)
    else:
        alumned = {
            'nom': alumne.nom,
            'cognoms': alumne.cognoms,
            'classe': alumne.classe.id_interna,
            'data_de_naixement': alumne.data_de_naixement,
            'correu_alumne': alumne.correu_alumne,
            'correu_pare': alumne.correu_pare,
            'correu_mare': alumne.correu_mare,
            'telefon_pare': alumne.telefon_pare,
            'telefon_mare': alumne.telefon_mare,
            'compartir': alumne.compartir
        }

    if is_admin(request.user):
        form = AlumneForms.AdminEditForm(alumned)
    else:
        alumned.update({'classe': alumne.classe})
        form = AlumneForms.EditForm(alumned, initial=alumned)
    context = {
        'form': form,
        'submitText': 'Actualitzar'
    }
    return render(request, 'contactboard/add.html', context)

@login_required
@user_passes_test(is_admin)
def delete_alumne(request, alumne_pk):
    alumne = get_object_or_404(Alumne, pk=alumne_pk)
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(alumne=alumne)
            if profile.user:
                profile.user.delete()
            if profile.unregisteredUser:
                profile.unregisteredUser.delete()
            profile.delete()
        except Profile.DoesNotExist:
            pass
        alumne.delete()
        return redirect('contactboard:list', alumne.classe.id_interna)
    context = {
        'alumne': alumne
    }
    return render(request, 'contactboard/delete-alumne.html', context)

@login_required
@user_passes_test(is_admin)
def mailto(request):
    if request.method == 'POST':
        form = MailtoForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            mailto_str = 'mailto:'
            if not cdata['no_cco']:
                mailto_str += '?bcc='
            for c in cdata['classes']:
                classe = Classe.objects.get(id_interna=c)
                for a in Alumne.objects.filter(classe=classe):
                    if (MailtoForm.TO_ALUMNES in cdata['enviar_a'] and
                        a.correu_alumne):
                        mailto_str += a.correu_alumne + ','
                    if (MailtoForm.TO_PARES in cdata['enviar_a'] and
                        a.correu_pare):
                        mailto_str += a.correu_pare + ','
                    if (MailtoForm.TO_MARES in cdata['enviar_a'] and
                        a.correu_mare):
                        mailto_str += a.correu_mare + ','
            while mailto_str[-1] == ',':
                mailto_str = mailto_str[:-1]
            response = HttpResponse()
            print(mailto_str)
            response.write(
                '<meta http-equiv="refresh" content="0; url={}" />'.format(
                    mailto_str))
            return response
    else:
        form = MailtoForm()
    context = {
        'form': form
    }
    return render(request, 'contactboard/mailto.html', context)

@login_required
@user_passes_test(is_admin)
def mailtoclasse(request, id_classe):
    classe = get_object_or_404(Classe, id_interna=id_classe)
    if request.method == 'POST':
        form = MailtoClasseForm(request.POST)
        if form.is_valid():
            cdata = form.cleaned_data
            mailto_str = 'mailto:'
            if not cdata['no_cco']:
                mailto_str += '?bcc='
            for a in Alumne.objects.filter(classe=classe):
                if (MailtoForm.TO_ALUMNES in cdata['enviar_a'] and
                    a.correu_alumne):
                    mailto_str += a.correu_alumne + ','
                if MailtoForm.TO_PARES in cdata['enviar_a'] and a.correu_pare:
                    mailto_str += a.correu_pare + ','
                if MailtoForm.TO_MARES in cdata['enviar_a'] and a.correu_mare:
                    mailto_str += a.correu_mare + ','
            while mailto_str[-1] == ',':
                mailto_str = mailto_str[:-1]
            response = HttpResponse()
            print(mailto_str)
            response.write(
                '<meta http-equiv="refresh" content="0; url={}" />'.format(
                    mailto_str))
            return response
    else:
        form = MailtoClasseForm()
    context = {
        'form': form,
        'classe': classe
    }
    return render(request, 'contactboard/mailto.html', context)
