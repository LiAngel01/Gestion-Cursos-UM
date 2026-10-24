from django.contrib import admin

from .models import MU, Student, Course, Matriculacion,Nota,NotaRegistrada,NotaFinal,MatriculacionR,NotaFinalR,CourseR,Usuario,NF,NFR
# Register your models here.

admin.site.register(MU)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Nota)
admin.site.register(Matriculacion)
admin.site.register(NotaRegistrada)
admin.site.register(NotaFinal)
admin.site.register(MatriculacionR)
admin.site.register(NotaFinalR)
admin.site.register(CourseR)
admin.site.register(Usuario)
admin.site.register(NF)
admin.site.register(NFR)