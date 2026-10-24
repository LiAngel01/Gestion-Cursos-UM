from pickle import NONE
from django.db import models
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator

# Create your models here.

class MU(models.Model):
    number = models.CharField(unique=True,verbose_name="Número",max_length=4, validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='El número debe tener exactamente 4 dígitos.'
            )
        ])
    provincia = models.CharField( null=True,blank=True,max_length=100,verbose_name="Región")     


 
    def __str__(self):
       return self.number

grados=(
    ('Soldado','Soldado'),
    ('Cabo','Cabo'),
    ('S3','S3'),
    ('S2','S2'),
    ('S1','S1'),
    ('Sargento P','Sargento P'),
    ('SubOficial','SubOficial'),
    ('SubTeniente','SubTeniente'),
    ('Teniente','Teniente'),
    ('Primer Teniente','Primer Teniente'),
    ('Capitán','Capitán'),
    ('Mayor','Mayor'),
    ('Teniente Coronel','Teniente Coronel'),
    ('Coronel','Coronel'),
)

class MUI(models.Model):
    number = models.CharField(unique=True,verbose_name="Número",max_length=4, validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='El número debe tener exactamente 4 dígitos.'
            )
        ])
    provincia = models.CharField( null=True,blank=True,max_length=100,verbose_name="Región")     


 
    def __str__(self):
       return self.number


Tipo_Curso = (
    ("Formación Oficiales"," Formación de Oficiales "),
    ("Especialistas Fundamentales","Especialistas Fundamentales"),
    ("Concentrados","Concentrados"),
    
)

class Course(models.Model):
    kind = models.CharField(max_length=200,verbose_name="Tipo de Curso",choices=Tipo_Curso, blank=False, null=True) 
    name = models.CharField(max_length=200,verbose_name="Curso") 
    start_date = models.DateField(null=True,verbose_name="Fecha de Inicio ( dd/mm/yyyy )")
    end_date = models.DateField(null=True,verbose_name="Fecha de fin ( dd/mm/yyyy )")
    description = models.TextField(max_length=1000,null=True,verbose_name="Descripción")
    isActive = models.BooleanField(default=True,blank=True)
    cantM = models.IntegerField(blank=True,null=True)
    
    def __str__(self):
       return self.name
    
    def calculate_total_m(self):
        
        self.cantM = Matriculacion.objects.filter(Course = self).count()
        return self.cantM
    
    
class CourseR(models.Model):
    name = models.CharField(max_length=200, unique=True,verbose_name="Curso") 
    start_date = models.DateField(null=True,verbose_name="Fecha de Inicio ( dd/m/yyyy ) ")
    end_date = models.DateField(null=True,verbose_name="Fecha de fin ( dd/m/yyyy )  ")
    description = models.TextField(max_length=1000,null=True,verbose_name="Descripción")
    
    def __str__(self):
       return self.name

Choices = (
    ('9no','9no'),
    ('12mo','12mo'),
    ('Nivel Superior','Nivel Superior'),
)
    
class Student(models.Model):
   CI = models.CharField( null=True, blank=False, max_length=11, unique=True,validators=[
            RegexValidator(
                regex=r'^\d{11}$|^\d{6}$',
                message='El número de cédula debe tener 11 o 6 dígitos.'
            )
        ] )
   firstName = models.CharField(max_length=100, verbose_name="Nombre" )  
   lastName = models.CharField(max_length=100, verbose_name="Primer Apellído")  
   seclastName = models.CharField(max_length=100, verbose_name="Segundo Apellído") 
   picture = models.ImageField(null=True,blank=True, verbose_name="Foto", upload_to="Img")
   MU = models.ForeignKey(MU, on_delete=models.CASCADE, verbose_name="UM de Procedencia")
   MUI = models.ForeignKey(MUI, on_delete=models.CASCADE, verbose_name="UM Menor ",null= True,blank=True)
   telefono = models.BigIntegerField(null=True, blank=True, verbose_name="Número de teléfono")
   matriculado = models.BooleanField(default=False,null=True,blank=True)
   nivelEscolar = models.CharField(max_length=20,choices=Choices,null=True,blank=False,verbose_name="Nivel Escolar")
   tomo = models.CharField(blank=False,null=True, max_length=5,verbose_name="Tomo" )
   folio = models.CharField(blank=False,null=True, max_length=5,verbose_name="Folio" )
   valoracion = models.TextField( null=True, blank=True,max_length=10000,verbose_name="Valoración")
   grado = models.CharField(choices=grados,max_length=50,null=True)
   
   def __str__(self):
        return self.firstName + " " + self.lastName
    

     
class Matriculacion(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="Curso")
    Student = models.ForeignKey(Student,on_delete=models.CASCADE,verbose_name="Estudiante")
    fecha = models.DateField(auto_now=True,null=True)
    primerExpediente= models.BooleanField(default=False,blank=True)
    def __str__(self):
        return self.Student.firstName + " en Curso de "+ self.Course.name 
    

class Nota(models.Model):
        Course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="Curso")
        Student = models.ForeignKey(Student,on_delete=models.CASCADE,verbose_name="Estudiante")
        note = models.PositiveIntegerField(null=False,default=2,validators=[
            MinValueValidator(2, message="La nota mínima es 2"),
            MaxValueValidator(5, message="La nota máxima es 5")
        ])
        
        valoracion = models.TextField( null=True, blank=True,max_length=10000, verbose_name="Resumen")
        tval = models.CharField(max_length=100,null=True, verbose_name="Tema Evaluado" ) 
        def __str__(self):
            return "Nota de "+ self.Student.firstName +" " + self.Student.lastName + " en el curso de "+ self.Course.name
        
       
        
from django.db.models import Avg

class NotaFinal(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Estudiante")
    final_note = models.FloatField(null=False, default=2, verbose_name="Nota Final",validators=[
            MinValueValidator(2, message="La nota mínima es 2"),
            MaxValueValidator(5, message="La nota máxima es 5")
        ])
    valoracion = models.TextField(null=True, blank=True, max_length=10000, verbose_name="Resumen")

    def __str__(self):
        return "Nota Final de " + self.Student.firstName + " " + self.Student.lastName + " en el curso de " + self.Course.name

    def calculate_final_note(self):
     student_notes = Nota.objects.filter(Course=self.Course, Student=self.Student)
     if student_notes.exists():
        notes_sum = sum(note.note for note in student_notes)
        dividendo = student_notes.count()
        if dividendo == 0:
            dividendo = 1
        self.final_note = round(notes_sum / dividendo)
        self.save()
        
     else:
        self.final_note = 2
        self.save()
     return self.final_note


class NotaRegistrada(models.Model):
        Course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="Curso")
        Student = models.ForeignKey(Student,on_delete=models.CASCADE,verbose_name="Estudiante")
        note = models.PositiveIntegerField(null=False,default=2,validators=[
            MinValueValidator(2, message="La nota mínima es 2"),
            MaxValueValidator(5, message="La nota máxima es 5")
        ])
        valoracion = models.TextField( null=True, blank=True,max_length=10000, verbose_name="Resumen")
        tval = models.CharField(max_length=100,null=True, verbose_name="Tema Evaluado" ) 
        def __str__(self):
            return "Nota de "+ self.Student.firstName +" " + self.Student.lastName + " en el curso de "+ self.Course.name 

class NotaFinalR(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Estudiante")
    final_note = models.PositiveIntegerField(null=False, default=2, verbose_name="Nota Final",validators=[
            MinValueValidator(2, message="La nota mínima es 2"),
            MaxValueValidator(5, message="La nota máxima es 5")
        ])
    valoracion = models.TextField(null=True, blank=True, max_length=10000, verbose_name="Resumen")
    
    def __str__(self):
        return "Nota Promedio de " + self.Student.firstName + " " + self.Student.lastName + " en el curso de " + self.Course.name
    
    def calculate_final_noteR(self):
     student_notes = NotaRegistrada.objects.filter(Course=self.Course, Student=self.Student)
     if student_notes.exists():
        notes_sum = sum(note.note for note in student_notes)
        dividendo = student_notes.count()
        dividendo -1
        if dividendo == 0:
           dividendo = 1;  
        self.final_note = round(notes_sum / dividendo)
        self.save()
     else:
        self.final_note = 2
        self.save()
     return self.final_note
    
    
class MatriculacionR(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="Curso")
    Student = models.ForeignKey(Student,on_delete=models.CASCADE,verbose_name="Estudiante")
    fecha = models.DateField( null=True)
    def __str__(self):
        return self.Student.firstName + " en Curso de "+ self.Course.name    

from django.contrib.auth.models import User


Options = (
    ('Admin','Administrador'),
    ('Colectivo','Colectivo'),
    ('Visitante','Visitante'),
    ('OyP','OyP')
)
 
class Usuario(User):
     rol= models.CharField( max_length=50,blank=False,null=True, choices=Options)
     
     
class NF(models.Model):
         fn = models.PositiveIntegerField(null=False, default=2, verbose_name="Nota Final",validators=[
            MinValueValidator(2, message="La nota mínima es 2"),
            MaxValueValidator(5, message="La nota máxima es 5")
        ])
         valoracion = models.TextField(null=True, blank=True, max_length=10000, verbose_name="Resumen")
         Course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
         Student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Estudiante")
         
         def __str__(self):
          return self.Student.firstName + " en Curso de "+ self.Course.name  
         
class NFR(models.Model):
         fn = models.PositiveIntegerField(null=False, default=2, verbose_name="Nota Final",validators=[
            MinValueValidator(2, message="La nota mínima es 2"),
            MaxValueValidator(5, message="La nota máxima es 5")
        ])
         valoracion = models.TextField(null=True, blank=True, max_length=10000, verbose_name="Resumen")
         Course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Curso")
         Student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Estudiante")   
         
         def __str__(self):
          return self.Student.firstName + " en Curso de "+ self.Course.name        