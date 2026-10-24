from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home',views.home, name="home" ),
    path('',views.MostrarPostLog, name="postlog"),
    path("courses",views.showCourses, name="courses"),
    path("students", views.showStudents, name="showStudents"),
    
    path("new-course ",views.newCourse, name="newCourse"),
    path("deleteCourse/<id>/", views.deleteCourse, name="deleteCourse"),
    path("modifyCourse/<id>/", views.modifyCourse, name="modifyCourse"),
    path("matriculadosEn/<id>/", views.matriculadosEnC , name="matriculadosEn"),
    path("close-course/<id>/", views.closeCourse , name="closeCourse"),
    path("reopen/<id>/", views.reopenCourse, name="reopenCourse"),
    path("closes-courses/", views.showClosesCourses, name="showClosesCourses"),
    path("course-data/<id>/", views.CourseData, name="CourseData"),
    path("course-ficha/<id>/", views.genFichaCourse, name="fichaCourse"),
    path("list-A/<id>/", views.listadoAprobados, name="listadoA"),
    path("list-NA/<id>/", views.listadoNoAprobados, name="listadoNA"),
    
    path("military-units",views.showMU , name="showMU"),
    path("newMU/", views.newMU, name="newMU"),
    path("modifyMU/<id>", views.modifyUM, name="modifyMU"),
    path("delete/<id>", views.deleteMU, name="deleteMU"),
    
    path("new-student",views.newStudent,name="newStudent"),
    path("deleteStudent/<id>/",views.deleteStudent,name="deleteStudent"),
    path("modify-student/<id>/", views.modifyStudent, name="modifyStudent"),
    path("student-data/<id>/", views.studentData, name="studentDetails"),
   #path("settingNote/<id>/",views.setNoteToStudent,name="settingNote"),
    path("matricular/<id>/", views.matricularEstudiante, name="matricular"),
    path("delete-mat/<id>/", views.deleteMat, name="deleteMat"),
    path("change-note/<id>", views.NoteToStudentByCourse, name="noteToStudent"),
    path("delete-note/<id>/",views.deleteNote, name="deleteNote"),
    #path("agregar-nf/<id>/", views.agregarNF, name="agregarNF"),
    path("modificar-nf/<id>/", views.modificarNF, name="modificarNF"),
    path("primer-expediente/<id>/",views.primer_expediente,name="primer_expediente"),
    
    path("valorar/<id>",views.AgregarValStudent, name="valToStudent"),
    path("ficha/<id>/", views.genFicha, name="genFicha")  ,
    path("agregar-nota/<id>/",views.add_note,name="add_note"), 
    path("changing-photo/<id>/", views.changePhoto, name="changePhoto"),
    path("no-mat/", views.showStudentsNotMat, name="studentsNotmat"),
    
   # path("titulo/<int:id>/",views.genTittle, name="genTittle"),
    path("studentsbycourse",views.studentsbyCourse, name="studentsbycourse"),
    
    path("loading-photo/<id>/", views.loadPhoto, name="loadPhoto"),
    path('screenshot/<id>/', views.screenshot, name='screenshot'),
    #path("title/<id>/",views.genTittle, name="genTittle"),
    #path('save-image/', views.save_screenshot, name='save_screenshot'), 
    
    path("new-User/",views.NewUser,name="NewUser"),
    path("user-list/",views.UserList,name="UserList"),
    path("modificar-user/<id>/",views.ModifyUser,name="modifyUser"),
    path("delete-user/<id>/",views.deleteUser,name="deleteUser")
]


