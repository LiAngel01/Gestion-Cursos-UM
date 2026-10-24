from django.shortcuts import render
from .models import Oficial,Postgrado
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OficialForm
from django.contrib.auth.decorators import login_required
from Cursos.models import Usuario
# Create your views here.
def index(request):
    
    post = Postgrado.objects.all()   
    oficiales=Oficial.objects.all()
    usuarios = Usuario.objects.all()
    data={
        'usuarios':usuarios,
        'entity':oficiales,
        'posts':post
    }
    
    if request.method =='POST':
       logout(request) 
       return redirect(to="/") 
    return render(request, "Unidad/index.html",data)


def ordenDelDia(request):
    return render(request,"Unidad/ordenDelDia.html")



@login_required
def pcdc(request):
    return  render(request,"Unidad/pcdc.html")

def galeria(request):
    return render(request,"Unidad/galeria.html")

def histórico(request):
    return render(request,"Unidad/histórico.html")

@login_required
def list_users(request):
    post = Postgrado.objects.all()
    oficiales=Oficial.objects.all()
    data={
        'entity':oficiales,
        'postgrado':post
    } 
    
    return render(request,"Unidad/users/userlist.html",data)

@login_required
def user_data(request,id):
    oficiales=Oficial.objects.all()
    oficial = get_object_or_404(Oficial,id=id)
    posts = Postgrado.objects.filter(user = oficial)
    data={
        'entity':oficiales,
        'oficial':oficial,
        'post':posts
    } 
    return render(request,"Unidad/users/userlist.html",data)

@login_required
def new_user(request):
    data={
      'form':OficialForm
    }
    if request.method == "POST":
        formulario = OficialForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="list_users")
    return render(request,"Unidad/users/userform.html",data)

@login_required
def delete_user(request,id):
    user = get_object_or_404(Oficial,id=id)
    user.delete()
    return redirect(to="list_users")

from .forms import PostgradoForm
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timezone
from dateutil.parser import parse

@login_required
def change_user(request, id):
    user = get_object_or_404(Oficial, id=id)
    posts = Postgrado.objects.all()
    formulario = OficialForm( instance=user)
    if request.method == "POST":
       if 'save_button' in request.POST: 
        formulario = OficialForm(data=request.POST, instance=user)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="list_users")       
       if 'delete_post' in request.POST:
            id = request.POST.get('delete_post')
            post=get_object_or_404(Postgrado,id=id)
            post.delete()     
            #Actualizar la fecha de nacimiento manualmente
            #fecha_nacimiento = request.POST.get('fecha_nacimiento')
            #if fecha_nacimiento:
                #user.fecha_nacimiento = parse(fecha_nacimiento).date()
                #user.save()
            user_id=user.pk
            return redirect(to="change_user",id=user_id)
       if 'agregar_post' in request.POST:       
            if request.POST['nombre_post']:
               n = request.POST['nombre_post']
               post = Postgrado.objects.create(
                user = user,
                nombre = n
            )

            
            user_id=user.pk
            redirect(to="change_user",id=user_id)
    else:
        if user.fecha_nacimiento == None:
            formulario = OficialForm(instance=user)
        else:    
            formulario = OficialForm(instance=user, initial={'fecha_nacimiento': user.fecha_nacimiento.strftime('%Y-%m-%d')})
        
    data = {
        'form': formulario,
        'user':user,
        'posts':posts,
        #'pform':PostgradoForm
         
    }
    return render(request, "Unidad/users/userform.html", data)


@login_required
def useCustomedForm(request):
    if request.method == 'POST':

       nombre = request.POST['nombre']
       ci = request.POST['CI']
       apellido = request.POST['apellido1']
       apellido2 = request.POST['apellido2']
       grado = request.POST['grado']
       graduadoDe = request.POST['GraduadoDe']
       direccion = request.POST['direccion']
       cargo = request.POST['cargo']
       nivel = request.POST['nivel']
       escuela = request.POST['escuela']
       fecha = request.POST['fecha']
       correo = None
       telefono = None
       if request.POST['correo']:
           correo = request.POST['correo']
           
       if request.POST['teléfono']:
           telefono = request.POST['teléfono']   
       if request.POST['postgrado']:
           postgrado = request.POST['postgrado'] 
        
       of,created = Oficial.objects.update_or_create(
           nombre = nombre,
           apellido = apellido,
           apellido2 = apellido2,
           CI = ci,
           grado = grado,
           graduadoDe = graduadoDe,
           cargo = cargo,
           escuelaProcedencia = escuela,
           correo = correo,
           telefono = telefono,
           direccion = direccion,
           nivel = nivel,
           fecha_nacimiento = fecha,
       )
       if request.POST['postgrado']:
        P = Postgrado.objects.create(
          user = of,
          nombre = postgrado 
        )
       postg = []
       i = 1
       while f'postgrado{i}' in request.POST:
            postgrado = request.POST[f'postgrado{i}']
            if postgrado:
                postg.append(postgrado)
            i += 1
       print(f"Cantidad de postgrados: {len(postg)}")
       
       for post in postg: 
        P = Postgrado.objects.update_or_create(
          user = of,
          nombre = post 
        )
        print(f"Postgrado: {postgrado}")

    return render(request,"Unidad/users/userCustomedForm.html")
from django.utils import timezone

from Cursos.models import Course

def eventos(request):
    time = timezone.now().date()
    
    cursos = Course.objects.filter(
        end_date__gt=time,
        start_date__lt=time
    )
    
    data = {
        'cursos':cursos
    }
    print(cursos)
   
    return render(request,"Unidad/eventos.html",data)