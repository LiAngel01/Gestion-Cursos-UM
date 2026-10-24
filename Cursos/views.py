from asyncio.windows_events import NULL
from pickle import NONE
from sqlite3 import Time
from tarfile import data_filter
from turtle import position
from django.shortcuts import render, redirect, get_object_or_404

from numpy import delete
from .models import Student, Course, MU,Matriculacion,Nota,NotaRegistrada,CourseR,Usuario,NF,NFR
from .forms import StudentForm,MUForm,CourseForm,CourseModForm,MatriculaForm,EvaluacionForm,valoracionForm,photoForm,UserForm,UserChangeForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import decorators
from django.core.paginator import Paginator
from django.http import Http404,HttpResponse
from django.core.files.base import ContentFile
import base64
import binascii
from io import BytesIO
import qrcode
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
# Create your views here.
from Cursos import templatetags


import time

def get_unique_param():
    return str(int(time.time()))

def update_everything():
    try:
        cursos = Course.objects.all()
        
        for curso in cursos:
            curso.calculate_total_m()
            curso.save()  # Asegúrate de guardar los cambios si es necesario
            
        print("Actualización completa de matriculas.")
        
        
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")

update_everything()

def home(request):
    return render(request, "Cursos/home.html")


import shutil
import os

@login_required
def MostrarPostLog(request):
    
    if request.method =='POST':
       logout(request) 
       return redirect(to="/") 
    update_everything()
    
    
    return render(request, "Cursos/postlog.html" )







@login_required
def showStudents(request):
    students = Student.objects.all()
    matriculaciones = Matriculacion.objects.all()
    
   
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search')
    course = request.GET.get('course_id')
    
    if course:
        matriculaciones = Matriculacion.objects.filter(Q(Course_id = course))
        students = [m.Student for m in matriculaciones]
        
        data = {
        'entity': students,
        'mat': matriculaciones,
        'courses': Course.objects.all(),
        'search_query': search_query,
        'course_id': course,
        
        
        }

        return render(request, "Cursos/Students/students.html", data)

    if search_query:
        students = Student.objects.filter(
            Q(firstName__icontains=search_query) |
            Q(lastName__icontains=search_query) |
            Q(seclastName__icontains=search_query) |
            Q(CI__icontains=search_query) |
            Q(MU__number__icontains=search_query)|
            Q(MUI__number__icontains=search_query)
        )
        students = [estudiante for estudiante in students if estudiante  in [m.Student for m  in matriculaciones]]  
        data = {
        'entity': students,
        'mat': matriculaciones,
        'courses': Course.objects.all(),
        'search_query': search_query,
        'course_id': course,
        'query':search_query,
        }

        return render(request, "Cursos/Students/students.html", data)
    
    students = [estudiante for estudiante in students if estudiante  in [m.Student for m  in matriculaciones]] 
    
    try:
        paginator = Paginator(students, 5)
        students = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'entity': students,
        'mat': matriculaciones,
        'courses': Course.objects.all(),
        'search_query': search_query,
        'course_id': course,
        'paginator':paginator
    }

    return render(request, "Cursos/Students/students.html", data)

from django.conf import settings
from django.shortcuts import render, redirect
from .forms import StudentForm
import cv2
import os
@login_required
def newStudent(request):
    data = {
        'form': StudentForm(),
        'formM':MatriculaForm()
    }
    
    
    if request.method == 'POST':
        formulario = StudentForm(data=request.POST)
        if formulario.is_valid(): 
         NO_curso = request.POST['Course']
         curso = get_object_or_404(Course, id=NO_curso)
         id_MU =  request.POST['MU']
         mu = get_object_or_404(MU, id = id_MU)
         
         telefono = request.POST['telefono'].strip()
         if telefono == '':
            telefono = None
         estudiante = Student.objects.create(
             CI = request.POST['CI'],
             firstName = request.POST['firstName'],
             lastName = request.POST['lastName'],
             seclastName = request.POST['seclastName'],
             MU= mu,
             telefono = telefono,
             tomo = request.POST['tomo'],
             folio = request.POST['folio'],
             nivelEscolar = request.POST['nivelEscolar'],
         )
         if not Matriculacion.objects.filter(Q(Course= curso )& Q(Student = estudiante) ):
        
           matriculacion=Matriculacion.objects.create(
           Course = curso, Student = estudiante
           )
           fecha_matriculacion = matriculacion.fecha
           NotaF= NF.objects.create(
              fn = 2,
              
              Student = estudiante,
              Course = curso
          )
           
           
           
           existing_notas_registradas = NotaRegistrada.objects.filter(Course=curso, Student=estudiante)
           for nota_registrada in existing_notas_registradas:
                Nota.objects.create(
                    Course=nota_registrada.Course,
                    Student=nota_registrada.Student,
                    note=nota_registrada.note,
                    valoracion=nota_registrada.valoracion,
                    tval=nota_registrada.tval
                )
                
               
         if not MatriculacionR.objects.filter(Q(Course= curso )& Q(Student = estudiante)):
           matR = MatriculacionR.objects.create(
           Course = curso, Student = estudiante,
           fecha= fecha_matriculacion 
        )
           
           NotaF= NFR.objects.create(
              fn = 2,
              
              Student = estudiante,
              Course = curso,
              
          )
           
         curso.calculate_total_m()
         curso.save() 
         estudiante.matriculado = True
         estudiante.save()
         formulario = StudentForm(data=request.POST, files=request.FILES)
         id = estudiante.id
         return redirect(to="studentDetails",id=id)
         '''
         # Captura la foto del estudiante utilizando OpenCV
         cap = cv2.VideoCapture(0)
         ret, frame = cap.read()
         cap.release()
            
         if ret:
                # Construye el nombre del archivo de la imagen
                foto_filename = f"{estudiante.CI}.jpg"
                foto_path = os.path.join('Img', foto_filename)
                
                try:
                    cv2.imwrite(os.path.join(settings.MEDIA_ROOT, foto_path), frame)
                except Exception as e:
                    print(f"Error guardando la imagen: {e}")
                    data["form"] = formulario
                    return render(request, "Cursos/Students/studentForm.html", data)
                
                # Guarda el estudiante en la base de datos
                #estudiante = formulario.save(commit=False)
                estudiante.picture = foto_path
                estudiante.save()
                id = estudiante.id
                return redirect(to="studentDetails",id=id)
         else:
                # Manejo del error de captura de imagen
                data["form"] = formulario
                return render(request, "Cursos/Students/studentForm.html", data)'''
        
        data["form"] = formulario
    return render(request, "Cursos/Students/studentForm.html", data)





@login_required
def deleteStudent(request,id):
    student = get_object_or_404(Student,id=id)
    student.delete()
    return redirect(to="showStudents")

@login_required
def studentData(request, id):
    
    student= Student.objects.get(id = id)
    notas= Nota.objects.all()
    matriculaciones = Matriculacion.objects.filter(Student = student)
    mat = Matriculacion.objects.filter(Student = student)
    notafr = NotaFinalR.objects.filter(Q(Student = student))
    notaf = NotaFinal.objects.filter(Q(Student = student))
    courses = MatriculacionR.objects.filter(Student = student)
    notasR = NotaRegistrada.objects.filter(Student = student)
    notafinal = NF.objects.filter(Student = student)
    notafinalr = NFR.objects.filter(Student = student)
    data = {
        'student': student,
        'entity':matriculaciones,
        'notas':notas,
        'notasR':notasR,
        'courses': courses,
        'notaf':notaf,
        'notafr':notafr,
        'mat': mat,
        'notafinal':notafinal,
        'notafinalr':notafinalr
        
    }
    
    return  render(request,"Cursos/Students/studentDetails.html", data )

@login_required
def deleteMat(request, id):
    matricula = get_object_or_404(Matriculacion, id=id)
    id= matricula.Student.id
    student=matricula.Student
    curso = matricula.Course
    nota = Nota.objects.filter( Q(Student = student) & Q(Course = curso)  )
    matriculaR = MatriculacionR.objects.filter(Q(Student = student) & Q(Course = curso) )
    notar = NotaRegistrada.objects.filter(Q(Student = student) & Q(Course = curso))
    notaf = NF.objects.filter((Q(Student = student) & Q(Course = curso)))
    if not notaf  :
        matriculaR.delete()
    nota.delete()
    notaf.delete()
    matricula.delete()
    curso.calculate_total_m()
    student.matriculado = False
    student.save()
    
    return redirect(to="studentDetails",id=id)

@login_required
def modifyStudent(request,id):
    student= get_object_or_404(Student, id=id)
    
    data= {
        'form':StudentForm(instance=student)
        
    }
    if request.method == 'POST':
      formulario = StudentForm(data=request.POST, instance=student,files=request.FILES)
      if formulario.is_valid():
            estudiante = formulario.save(commit=False)
            estudiante.save()
                
            return redirect(to="studentDetails",id=id)
      else:
                
                data["form"] = formulario
                
      
    
    return render(request,"Cursos/Students/studentModForm.html", data )

@login_required
def AgregarValStudent(request,id):
    estudiante = get_object_or_404(Student, id=id)
    data={
         'entity':estudiante,
        'form':valoracionForm(instance= estudiante)
    }
    if request.method =='POST':
      formulario = valoracionForm(data=request.POST,instance=estudiante)
      if formulario.is_valid():
          formulario.save()
          return redirect(to="studentDetails",id=id)
      else:
          data["form"] = formulario 
    return render(request,"Cursos/Students/valoracion.html",data)

from .models import MatriculacionR

@login_required
def matricularEstudiante(request,id):
    estudiante = get_object_or_404(Student, id=id)
    
    courses = Course.objects.all()
    data={
        'student':estudiante,
        'courses':courses,
        'form':MatriculaForm()
    }
    if request.method == 'POST':
      NO_curso = request.POST['Course']
      curso = get_object_or_404(Course, id=NO_curso)
      
      if not Matriculacion.objects.filter(Q(Course= curso )& Q(Student = estudiante) ):
        
        matriculacion=Matriculacion.objects.create(
           Course = curso, Student = estudiante
        )
        print(matriculacion.fecha)
        fecha_matriculacion = matriculacion.fecha
        NotaF= NF.objects.create(
              fn = 2,
              
              Student = estudiante,
              Course = curso
              
          )
        
        
        existing_notas_registradas = NotaRegistrada.objects.filter(Course=curso, Student=estudiante)
        for nota_registrada in existing_notas_registradas:
                Nota.objects.create(
                    Course=nota_registrada.Course,
                    Student=nota_registrada.Student,
                    note=nota_registrada.note,
                    valoracion=nota_registrada.valoracion,
                    tval=nota_registrada.tval
                )
      if not MatriculacionR.objects.filter(Q(Course= curso )& Q(Student = estudiante)):
           matR = MatriculacionR.objects.create(
           Course = curso, Student = estudiante,
           fecha = fecha_matriculacion
        )
           
      if not NFR.objects.filter(Q(Course= curso )& Q(Student = estudiante)):
               NotaFR= NFR.objects.create(
              fn = 2,
              
              Student = estudiante,
              Course = curso
              
          )
           
      if  MatriculacionR.objects.filter(Q(Course= curso )& Q(Student = estudiante)):
          matR = MatriculacionR.objects.get(Q(Course= curso )& Q(Student = estudiante))
          matR.fecha= fecha_matriculacion
          matR.save()
      curso.calculate_total_m()
      curso.save()
      estudiante.matriculado = True
      estudiante.save()
          
           
           
      ''''nota = Nota.objects.create(
          Course = curso, Student = estudiante,
          
        )'''
           
      return redirect(to="studentDetails",id = id)
      
    return render(request, "Cursos/Students/matricular.html",data)



def deleteNote(request, id):
    note = get_object_or_404(Nota, id=id)
    id_student = note.Student.id
    noter = NotaRegistrada.objects.filter(
        Course=note.Course,
        Student=note.Student,
        tval=note.tval,
        valoracion=note.valoracion,
        note=note.note
    )
    noter.delete()
    note.delete()

    try:
        nota_final = NotaFinal.objects.get(
            Course=note.Course,
            Student=note.Student
        )
        
    except NotaFinal.DoesNotExist:
        nota_final = None

    if nota_final:
        nota_final.calculate_final_note()
        nota_final.save()
        if nota_final.final_note == 2:
            nota_final.delete()
            print("borrando promedio")
    try:
        nota_final_r = NotaFinalR.objects.get(
            Course=note.Course,
            Student=note.Student
        )    
    except NotaFinalR.DoesNotExist:
        nota_final = None
        
    if nota_final_r:
        nota_final_r.final_note = nota_final.final_note
        nota_final_r.save()    
        if nota_final_r.final_note == 2:
            nota_final_r.delete() 
    return redirect(to="studentDetails", id=id_student)

   #return studentData(request,id = id_student )


from django.contrib import messages
@login_required
def add_note(request, id):
    matric = get_object_or_404(Matriculacion, id= id)
    id_curso = matric.Course.id
    id_student = matric.Student.id
    course = get_object_or_404(Course, id=id_curso)
    student = get_object_or_404(Student,id=id_student)
    
    data = {'form': EvaluacionForm,
            'course': course, 
            'student': student}
    
    if request.method == 'POST':
        form = EvaluacionForm(data=request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            
            note.Course = course
            note.Student = student
            if Nota.objects.filter(Course=course, Student=student, tval=note.tval).exists():
                messages.error(request, "Ya existe una nota con el mismo curso, estudiante y tema.")
                return render(request, "Cursos/Students/noteToStudent.html", {'form': form, 'course': course, 'student': student})
            note.save()
            # para las notas registradas
            value = note.note
            curso = note.Course 
            estudiante = note.Student
           
            
            nota_registrada, created = NotaRegistrada.objects.update_or_create(
                Course=course,
                Student=student,
                tval=note.tval
            )
            nota_registrada.note = note.note
            nota_registrada.valoracion = note.valoracion
            nota_registrada.save()  
            
            nota_final, created = NotaFinal.objects.update_or_create(
                Course=curso,
                Student=estudiante
            )
            try:
              nota_final = NotaFinal.objects.get(Course=curso, Student=estudiante)
            except NotaFinal.DoesNotExist:
              nota_final = NotaFinal.objects.create(Course=curso, Student=estudiante)

            nota_final.calculate_final_note()
            nota_final.save()
            
            nota_finalR, created = NotaFinalR.objects.get_or_create(
                Course=curso,
                Student=estudiante
            )
            nota_finalR.calculate_final_noteR()
            nota_finalR.save()
            
            
            fil = NotaFinalR.objects.filter(Course=curso, Student=estudiante,) 
            if fil:     
              for notaFR in fil:
                 notaFR.Course = curso
                 notaFR.Student = estudiante
                 notaFR.final_note = nota_finalR.final_note   
                 
            else:
             notafr = NotaFinalR.objects.create( Course=curso, 
                                               Student=estudiante, 
                                               final_note = nota_finalR.final_note )
         
            return redirect('studentDetails',id=id_student)
    else:
        form = EvaluacionForm()

    return render(request, "Cursos/Students/noteToStudent.html", data)

@login_required
def NoteToStudentByCourse(request,id):
    
    nota = get_object_or_404(Nota,id=id)
    estudiante = nota.Student
    curso = nota.Course
    temav = nota.tval
    filtro =  NotaRegistrada.objects.filter(Q(Course= curso )& Q(Student = estudiante)& Q(tval = temav) )
    print(nota)
    data ={
        'course':curso,
        'student':estudiante,
        'nota':nota,
        'form':EvaluacionForm(instance=nota)
    }
    
    if request.method == 'POST':
      formulario = EvaluacionForm(data=request.POST, instance=nota)
      
      if formulario.is_valid():
         formulario.save()
         
         nota_final, created = NotaFinal.objects.get_or_create(
                Course=nota.Course,
                Student=nota.Student
            )
         nota_final.calculate_final_note()
         nota_final.save()
         
         value = nota.note
         curso = nota.Course 
         estudiante = nota.Student
         resumen = nota.valoracion
         temav = nota.tval
         
         if filtro: 
             for nota_registrada in filtro:
                 nota_registrada.note = value
                 nota_registrada.valoracion = resumen
                 nota_registrada.tval = temav
                 nota_registrada.save()
         else:
             notaR = NotaRegistrada.objects.create(
                 Course = curso, Student = estudiante, note= value, tval = temav, valoracion = resumen
             )  
         fil = NotaFinalR.objects.filter(Course=curso, Student=estudiante,) 
         if fil:     
            for notaFR in fil:
                 notaFR.Course = curso
                 notaFR.Student = estudiante
                 notaFR.final_note = nota_final.final_note   
                 
         else:
            notafr = NotaFinalR.objects.create( Course=curso, 
                                               Student=estudiante, 
                                               final_note = nota_final.final_note )  
          
         id=nota.Student.id    
         return redirect(to="studentDetails",id=id)
         
         
      else: 
          data["form"] = formulario   
    
    return render(request,"Cursos/Students/noteToStudent.html",data )




from .models import NotaFinal

@login_required
def update_final_note(request, course_id, student_id):
    nota_final, _ = NotaFinal.objects.get_or_create(Course_id=course_id, Student_id=student_id)
    nota_final.calculate_final_note()
    return redirect('course_detail', course_id=course_id)


#################################################### Courses ##################################################


@login_required
def showCourses(request):
    
    courses = Course.objects.filter(isActive = True)
    queryset = request.GET.get("search")

    if queryset:
        courses = Course.objects.filter(Q(name__icontains = queryset))
        
        data = {
        'entity': courses,
        'query':queryset,
        }
        
        return render(request, "Cursos/Courses/courses.html", data)
    
    
    
    
    data = {
        'entity': courses,
        'query':queryset,
        
    }
    
    return render(request, "Cursos/Courses/courses.html", data) 

@login_required
def matriculadosEnC(request,id):
    
    curso = get_object_or_404(Course,id=id)
    matricula = Matriculacion.objects.filter(Course = curso)
    cant = Matriculacion.objects.filter(Course = curso).count()
    nota = Nota.objects.filter(Course = curso)
    notaf =NF.objects.filter(Course = curso)
    
    
    data={
        'notaf':notaf,
        'nota':nota,
        'curso':curso,
        'entity':matricula,
        'cant':cant
     }
    return render(request, "Cursos/Courses/matriculadosEn.html",data)

@login_required
def CourseData(request,id):
    curso = get_object_or_404(Course,id=id)
    matricula = MatriculacionR.objects.filter(Course = curso)
    cantM = matricula.count()
    data={
        
        'curso':curso,
        'entity':matricula,
        'cantM':cantM
     }
    return render(request,"Cursos/Courses/course_data.html",data) 

   
@login_required
def newCourse(request):
    
    data = { 'form': CourseForm  }
    
    if request.method == 'POST':
        formulario = CourseForm(data=request.POST)
        
        if formulario.is_valid():
           
           name = request.POST['name']
           start_date = formulario.cleaned_data.get('start_date')
           end_date = formulario.cleaned_data.get('end_date')
           description = request.POST['description']
            
           formulario.save()
           
           ''''
           cr=CourseR.objects.create(
               name = name,
               start_date = start_date,
               end_date = end_date,
               description = description
           )'''
           
           return redirect( to="courses" )
           
        else:
            data["form"] = formulario   
        
    return render(request,"Cursos/Courses/CourseForm.html", data) 

@login_required
def modifyCourse(request, id):
    
    curso =  get_object_or_404(Course, id=id)
    
    data = {'form':CourseModForm(instance=curso)}
    
    if request.method=='POST':
        formulario = CourseModForm(data=request.POST, instance=curso )
        if formulario.is_valid():
           formulario.save()
           return redirect( to="courses" )
        else:
          data["form"] = formulario    
   # else:
     #   if curso.start_date == None:
         #   formulario = CourseForm(instance=curso)
       # else:    
          #  formulario = CourseForm(instance=curso, initial={'start_date': curso.start_date.strftime('%Y-%m-%d')})
        
           
    
    return render(request,"Cursos/Courses/CourseForm.html", data) 

@login_required
def deleteCourse(request, id):
   course= get_object_or_404(Course,id=id)
   course.delete()
   return redirect( to="showClosesCourses" )
 
@login_required
def closeCourse(request,id):
     course= get_object_or_404(Course,id=id)
     course.isActive = False
     course.save()
     return redirect( to="courses" )
 
@login_required 
def showClosesCourses(request):
    
    cursos = Course.objects.all()
    queryset = request.GET.get("search")

    if queryset:
        cursos = Course.objects.filter(Q(name__icontains = queryset)|Q(start_date__icontains = queryset)|Q(end_date__icontains = queryset))
    
    
    data={
        'entity':cursos
    }
    
    return render(request,"Cursos/Courses/Closes_Courses.html",data) 

@login_required
def reopenCourse(request,id):
    curso= get_object_or_404(Course, id = id)
    curso.isActive = True
    curso.save()
    return redirect( to="showClosesCourses" )
    
    
 ################################################ U-M ##################################################   
  
@login_required  
def showMU(request):
    mu = MU.objects.all()
    page = request.GET.get('page', 1)
    queryset = request.GET.get("search")
    
   
    
    
    if queryset:
        mu = MU.objects.filter(number__icontains = queryset)
    
    try:
        paginator = Paginator(mu, 5)
        mu = paginator.page(page)
    except:
        raise Http404
    
    data= {
        'entity':mu,
        'paginator':paginator 
    }
    
    return render(request,"Cursos/MU/military_units.html", data)     
    
    
@login_required 
def newMU(request):
    
    data = { 'form': MUForm  }
    
    if request.method == 'POST':
        formulario = MUForm(data=request.POST)
        
        if formulario.is_valid():
           formulario.save()
           return redirect(to="showMU") 
           
        else:
            data["form"] = formulario 
             
        
    
    return render(request,"Cursos/MU/newMU.html", data) 

@login_required
def modifyUM(request, id):
    mu = get_object_or_404(MU, id=id)
    
    data = {'form':MUForm(instance=mu)}
    
    if request.method=='POST':
        formulario = MUForm(data=request.POST, instance=mu )
        if formulario.is_valid():
           formulario.save()
           return redirect(to="showMU") 
        else:
           data["form"] = formulario
            
    
    return render(request,"Cursos/MU/modifyMU.html", data) 

@login_required
def deleteMU(request,id):
    mu=get_object_or_404(MU, id=id)
    mu.delete()
    return redirect(to="showMU" )

@login_required
def searchStudent(request):
    queryset = request.GET.get("search")
    if queryset:
           student = Student.objects.filter(Q(firstName__icontains = queryset)|
                                    Q(lastName__icontains=queryset)|
                                    Q(seclastName__icontains = queryset)|
                                    Q(CI__icontains = queryset))
    
    data={
        'students':student
    }
    
    return render(request,"Cursos/Students/students.html",data)

@login_required
def genFicha(request,id):
    student= Student.objects.get(id = id)
    notas= Nota.objects.all()
    matriculaciones = Matriculacion.objects.all()
    notafr = NotaFinalR.objects.filter(Q(Student = student))
    notaf = NotaFinal.objects.filter(Q(Student = student))
    courses = MatriculacionR.objects.filter(Student = student)
    notasR = NotaRegistrada.objects.filter(Student = student)
    data = {
        'student': student,
        'entity':matriculaciones,
        'notas':notas,
        'notasR':notasR,
        'courses': courses,
        'notaf':notaf,
        'notafr':notafr,
        
    }
    return render(request,"Cursos/Students/ficha.html", data)

from django.views.decorators.cache import never_cache
from django.utils.cache import patch_cache_control

@login_required
@never_cache
def changePhoto(request, id):
    person = get_object_or_404(Student, id=id)
    photo_error = None

    if request.method == 'POST':
        photo_data = request.POST.get('photo', '')
        header, separator, encoded = photo_data.partition(',')

        if header != 'data:image/jpeg;base64' or not separator or not encoded:
            photo_error = 'No se recibió una foto válida. Captúrala nuevamente.'
        else:
            try:
                file_data = base64.b64decode(encoded, validate=True)
            except (binascii.Error, ValueError):
                photo_error = 'La foto recibida está dañada. Captúrala nuevamente.'
            else:
                try:
                    with Image.open(BytesIO(file_data)) as image:
                        image_format = image.format
                        image.verify()
                except (UnidentifiedImageError, OSError):
                    photo_error = 'El archivo recibido no es una imagen válida.'
                else:
                    if image_format != 'JPEG':
                        photo_error = 'La cámara debe enviar la foto en formato JPEG.'
                    else:
                        person.picture.save(f'{person.CI}.jpg', ContentFile(file_data), save=True)
                        return redirect(to="studentDetails", id=id)

    data = {
        'student': person,
        'photo_error': photo_error,
    }
    return render(request, "Cursos/Students/foto_edit.html", data)





from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Nota, NotaFinal,NotaFinalR


@login_required
@receiver(post_save, sender=Nota)
def update_final_note(sender, instance, **kwargs):
    try:
        nota_final = NotaFinal.objects.get(Course=instance.Course, Student=instance.Student)
        nota_final.calculate_final_note()
    except NotaFinal.DoesNotExist:
        # Si no existe una entrada en NotaFinal, la creas
        nota_final = NotaFinal.objects.create(
            Course=instance.Course,
            Student=instance.Student
        )
        
        nota_final.calculate_final_note()
        
@login_required        
def showStudentsNotMat(request):
    students = Student.objects.all()
    matriculaciones = Matriculacion.objects.all()
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search')
    
     
    if search_query:
        students = students.filter(
            Q(firstName__icontains=search_query) |
            Q(lastName__icontains=search_query) |
            Q(seclastName__icontains=search_query) |
            Q(CI__icontains=search_query) |
            Q(MU__number__icontains=search_query)
        )
    # Crear una lista de estudiantes que no tienen una matriculación
    estudiantes_no_matriculados = [estudiante for estudiante in students if estudiante not in [m.Student for m in matriculaciones]]
   
    
    try:
        paginator = Paginator(estudiantes_no_matriculados,5)
        estudiantes_no_matriculados = paginator.page(page)
        
    except:
        raise Http404
    
    data = {
        'students': estudiantes_no_matriculados,
        'entity': matriculaciones,
        'courses': Course.objects.all(),
        'search_query': search_query,
        'paginator':paginator
    }

    return render(request, "Cursos/Students/list_no_matricualdos.html", data)  
  
  
@login_required
def studentsbyCourse(request):
    students = Student.objects.all()
    matriculaciones = Matriculacion.objects.all()
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search')
    course = request.GET.get('course_id')
    
   

    if search_query:
        students = students.filter(
            Q(firstName__icontains=search_query) |
            Q(lastName__icontains=search_query) |
            Q(seclastName__icontains=search_query) |
            Q(CI__icontains=search_query) |
            Q(MU__number__icontains=search_query)
        )

    if course:
        matriculaciones = Matriculacion.objects.filter(Q(Course_id = course))
        students = [m.Student for m in matriculaciones]
    
    try:
        paginator = Paginator(students, 5)
        students = paginator.page(page)
    except:
        raise Http404
    
    data = {
        'student': students,
        'entity': matriculaciones,
        'courses': Course.objects.all(),
        'search_query': search_query,
        'course_id': course,
        'paginator':paginator
    }

    return render(request, "Cursos/Colectivo/StudentsByCourse.html",data )


@login_required
def loadPhoto(request, id):
    estudiante = get_object_or_404(Student, id=id)
    data = {
        'estudiante': estudiante,
        'form': photoForm(instance=estudiante),
    }
    if request.method == 'POST':
        formulario = photoForm(instance=estudiante, data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="studentDetails", id=estudiante.id)
        else:
            data['form'] = formulario

    return render(request, "Cursos/Students/photoForm.html", data)


from django.http import HttpResponse
from django.template.loader import render_to_string    
from django.utils import timezone,dates
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
import qrcode
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import os
import qrcode
from datetime import datetime
from .models import Matriculacion
from django.conf import settings
def obtener_mes(mes):
    """
    Función auxiliar para obtener el nombre del mes a partir del número.
    """
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    return meses[mes - 1]

def screenshot(request, id):
    """
    Vista mejorada para generar certificados con texto perfectamente centrado
    """
    matricula = get_object_or_404(Matriculacion, id=id)
    
    # Configuración inicial
    hoy = datetime.today().day
    mes = datetime.today().month
    mes_nombre = obtener_mes(mes)
    year = datetime.today().year

    # --- Generación del QR (se mantiene igual) ---
    qr_data = f"Certificado de {matricula.Student} - {matricula.Course}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # --- Carga de imágenes ---
    fondo_path = os.path.join(settings.BASE_DIR, 'Cursos', 'static', 'Cursos', 'img', 'Presentación7.jpg')
    certificado_img = Image.open(fondo_path).copy()
    draw = ImageDraw.Draw(certificado_img)
    
    # --- Fuentes (ajusta las rutas según tu proyecto) ---
    font_titulo = ImageFont.truetype('arial.ttf', size=38)
    font_normal = ImageFont.truetype('arial.ttf', size=16)
    font_secundario = ImageFont.truetype('arial.ttf', size=16)
    
    # --- Sistema de centrado mejorado ---
    def texto_centrado(texto, y_pos, font, fill="black"):
        """Función helper para texto perfectamente centrado"""
        draw.text(
            (certificado_img.width // 2, y_pos),  # X centrado
            texto,
            fill=fill,
            font=font,
            anchor="mm"  # Magic! Centra horizontal y verticalmente
        )
    
    # --- Textos del certificado ---
    # Título principal
    texto_centrado("CERTIFICADO", 220, font_titulo)
    
    # Datos del estudiante
    texto_centrado(f"A: {matricula.Student} {matricula.Student.seclastName}", 280, font_normal)
    
    # Tipo de curso (con lógica condicional mejorada)
    tipo_curso = {
        "Concentrados": f"Curso de Concentrado de {matricula.Course}",
        "Especialistas Fundamentales": f"Curso de Especialistas Fundamentales de {matricula.Course}",
        "Formación Oficiales": f"Curso de Formación Oficiales de {matricula.Course}"
    }.get(matricula.Course.kind, f"Curso: {matricula.Course}")
    
    texto_centrado(tipo_curso, 310, font_secundario)
    texto_centrado("Especialidad de Comunicaciones.", 340, font_secundario)
    
    # Primer expediente (condicional)
    if matricula.primerExpediente:
        texto_centrado("Resultando ser el Primer Expediente", 370, font_secundario)
    
    # Fecha (formato mejorado)
    texto_centrado(f"Dado en La Habana, a los {hoy} días del mes {mes_nombre} de {year}", 400, font_secundario)
    
    # --- QR y firmas (se mantienen igual) ---
    qr_img = qr_img.resize((150, 150))
    certificado_img.paste(qr_img, ((certificado_img.width - qr_img.width) // 2, 450))
    
    # --- FIRMAS (VERSIÓN ORIGINAL) ---
# Jefe Colectivo Profesores (posición izquierda)
    draw.text((150, 560), " ____________________", fill="black", font=font_secundario)
    draw.text((150, 580), "Jefe Colectivo Profesores", fill="black", font=font_secundario)
    draw.text((150, 600), " Cp Dariel Peña Martínez", fill="black", font=font_secundario)

# Jefe Unidad Militar (posición derecha)
    draw.text((650, 560), "____________________", fill="black", font=font_secundario)
    draw.text((650, 580), "    Jefe Unidad Militar", fill="black", font=font_secundario)
    draw.text((650, 600), "My José Javier Martínez León", fill="black", font=font_secundario)
    # --- Guardado y respuesta (se mantiene igual) ---
    response = HttpResponse(content_type="image/png")
    certificado_img.save(response, format="PNG")
    response['Content-Disposition'] = f'attachment; filename="certificado_{id}.png"'
    return response






    

#
# #
# #
@login_required
def NewUser(request):
    
    data={
        'form': UserForm
    }
    if request.method== 'POST':
        formulario = UserForm(data=request.POST)
        if formulario.is_valid():
           formulario.save()
           return redirect(to="UserList")  
        else:
           data["form"] = formulario  
    return render(request, "Cursos/Users/UserForm.html",data) 

@login_required
def UserList(request):
    users = Usuario.objects.all()
    data={
        'entity':users
    }
    return render(request, "Cursos/Users/UserList.html",data) 

@login_required
def ModifyUser(request,id):
    usuario = get_object_or_404(Usuario, id=id)
    
    data={
        'form':UserChangeForm(instance=usuario)
    }
    if request.method == 'POST':
      formulario= UserChangeForm(instance = usuario ,data=request.POST)
      if formulario.is_valid():
         formulario.save()
         return redirect(to="UserList")
      else:
         data["form"]=formulario  
    return render(request,"Cursos/Users/UserForm.html",data)

@login_required
def deleteUser(request,id):
    usuario = get_object_or_404(Usuario,id=id)
    usuario.delete()
    return redirect(to="UserList")


@login_required
def genFichaCourse(request,id):
    curso = get_object_or_404(Course, id=id)
    curso.calculate_total_m()
    matricula = Matriculacion.objects.filter(Course = curso).select_related('Student').order_by('Student__firstName')
    nf = NFR.objects.filter(Course = curso)  
    #numeros = list(range(1, len(matricula) + 1))     
    data={
        'curso':curso,
        'matricula':matricula,
        'nf':nf
       
    }
    # Renderiza el HTML de la página que quieres capturar
    html = render_to_string("Cursos/Courses/ficha_course.html", data)
    # Devuelve la respuesta HTTP con el HTML
    return HttpResponse(html, content_type="text/html")
    #return render(request, "Cursos/Courses/ficha_course.html",data)


from .forms import NFForm

def modificarNF(request, id):
    nota = get_object_or_404(NF, id=id)
    estudiante = nota.Student
    idstd = estudiante.id
    curso = nota.Course
    data = {
        'form': NFForm(instance=nota),
        'course': curso,
        'student': estudiante
    }
    
    if request.method == 'POST':
        formulario = NFForm(data=request.POST, instance=nota)  # Usar instance aquí
        if formulario.is_valid():
            fn = formulario.cleaned_data["fn"]
            valoracion = formulario.cleaned_data["valoracion"]
            formulario.save()  # Guardar el formulario directamente
            
             # Actualizar o crear la nota final registrada
            notafinalr, created = NFR.objects.update_or_create(
                Student=estudiante,
                Course=curso,
                defaults={
                    'fn': fn,
                    'valoracion': valoracion
                }
            )
                
            return redirect(to="studentDetails", id=idstd)
        else:
            data["form"] = formulario

    return render(request, "Cursos/Students/noteToStudent.html", data)



def listadoAprobados(request,id):
    curso = get_object_or_404(Course, id=id)
    list = Matriculacion.objects.filter( Course = curso ) 
    notas = NF.objects.all()
    data = {
        'lista':list,
        'notas':notas,
        'curso':curso
    }
    return render(request,"Cursos/Courses/listadoAprobados.html",data)

def listadoNoAprobados(request,id):
    curso = get_object_or_404(Course, id=id)
    list = Matriculacion.objects.filter( Course = curso ) 
    notas = NF.objects.all()
    data = {
        'curso':curso,
        'lista':list,
        'notas':notas
    }
    return render(request,"Cursos/Courses/listadoNoAprobados.html",data)


def primer_expediente(request,id):
        
    matricula = get_object_or_404(Matriculacion,id=id)
    if matricula.primerExpediente == True:
       matricula.primerExpediente = False
    else:
       matricula.primerExpediente = True
    matricula.save()
    print(matricula.primerExpediente)
    id=matricula.Student.id
    return  redirect(to="studentDetails",id=id)

    