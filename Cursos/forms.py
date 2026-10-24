from pyexpat import model
from .models import Student, MU,Course,Matriculacion,Nota,Usuario,NF
from django import forms 
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ["firstName","lastName","seclastName","telefono","MU","MUI","CI","nivelEscolar","tomo","folio","grado"]


class MUForm(forms.ModelForm):
    class Meta:
        model = MU
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%d/%m/%Y'
        super().__init__(**kwargs)

        
class CourseForm(forms.ModelForm):
    
    class Meta:
        model = Course
        fields =  ["kind","name","start_date", "end_date", "description"]
        widgets = {
            #'start_date': forms.DateInput(attrs={'type': 'date'}),
            #'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        startd = cleaned_data.get('start_date')
        endd = cleaned_data.get('end_date')
        name = cleaned_data.get('name')

        # Verifica si ya existe una nota con los mismos valores de course, student y tval
        if Course.objects.filter(name = name, start_date = startd,end_date = endd).exists():
            raise forms.ValidationError("Ya existe ese Curso .")

        return cleaned_data           
        
class CourseModForm(forms.ModelForm):
    
    class Meta:
        model = Course
        fields =  ["kind","name","start_date", "end_date", "description"]
        widgets = {
            #'start_date': forms.DateInput(attrs={'type': 'date'}),
            #'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
            
class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matriculacion
        fields = ["Course"]                           
     
    def __init__(self, *args, **kwargs):
        super(MatriculaForm, self).__init__(*args, **kwargs)
        self.fields['Course'].queryset = Course.objects.filter(isActive=True)
     
class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ["note","tval","valoracion"]    
        
    def clean(self):
        cleaned_data = super().clean()
        tval = cleaned_data.get('tval')
        course = cleaned_data.get('Course')
        student = cleaned_data.get('Student')

        # Verifica si ya existe una nota con los mismos valores de course, student y tval
        if Nota.objects.filter(Course=course, Student=student, tval=tval).exists():
            raise forms.ValidationError("Ya existe esa Nota.")

        return cleaned_data    
        
class valoracionForm(forms.ModelForm):
    class Meta:
        model= Student
        fields=["valoracion"]        
        
class  photoForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=["picture"]         
        
        
class UserForm(UserCreationForm):
    class Meta:
        model=Usuario
        fields=["username","rol"]        
        
class UserChangeForm(UserChangeForm):
    class Meta:
        model=Usuario
        fields=["username","rol"]         
        
class NFForm(forms.ModelForm):
    class Meta:
        model = NF
        fields=["fn","valoracion"]        