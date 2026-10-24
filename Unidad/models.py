from django.db import models
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
# Create your models here.

Choices=(
    ('SubOficial','SubOficial'),
    ('SubTeniente','SubTeniente'),
    ('Teniente','Teniente'),
    ('Primer Teniente','Primer Teniente'),
    ('Capitán','Capitán'),
    ('Mayor','Mayor'),
    ('Teniente Coronel','Teniente Coronel'),
    ('Coronel','Coronel'),
)
Options=(
    ('Jefe U/M','Jefe U/M'),
    ('2do Jefe U/M','2do Jefe U/M'),
    ('Político','Político' ),
    ('OyP','OyP'),
    ('Jefe Colectivo Profesores','Jefe Colectivo Profesores'),
    ('Jefe Centro 1', 'Jefe Centro Comones 1'),
    ('Jefe Subcentro Comones ','Jefe Subcentro Comones 1'),
    ('Jefe Grupo Carro Mando','Jefe Grupo Carro Mando'),
    ('Técnico Radios','Técnico Radios'),
    ('Jefe Sala Comunicaciones Móvil','Jefe Sala Comunicaciones Móvil'),
    ('Jefe Grupo Tele-Comunicaciones','Jefe Grupo Tele-Comunicaciones'),
    ('Jefe Grupo Telefónico','Jefe Grupo Telefónico'),
    
    ('Jefe SubCentro Cifras','Jefe SubCentro Cifras'),
    ('Técnico Cifras','Técnico Cifras'),
    ('Jefe Grupo Cifras','Jefe Grupo Cifras'),
    
    ('Subcentro de Apoyo','Subcentro de Apoyo'),
    ('Jefe Grupo Comunicaciones Apoyo','Jefe Grupo Comunicación Apoyo'),
    
    ('Puesto MT','Puesto MT'),
    ('Jefe Centro 2', 'Jefe Centro Comones 2'),
    ('Jefe Subcentro Comones 2','Jefe Subcentro Comones 2'),
    ('Colectivo','Colectivo'),
    ('Ingeniero Principal','Ingeniero Principal'),
    ('Técnico Tanques y Transporte','Técnico Tanques y Transporte'),
    ('Logística','Logística'),
    ('Ingeniero Principal CC1','Ingeniero Principal CC1'),
)

Escuelas = (
    ('ITM','ITM José Martí'),
    ('EIFAM','Escuela Inter-Armas de las FAR Antonio Maceo '),
    ('EIFJM','Escuela Inter-Armas de las FAR josé Maceo '),
    ('UCI','UCI'),
    ('CUJAE','CUJAE'),
    ('UH','UH'),
    ('UM 4261','UM 4261'),
    
)
Niveles = (
    ('Nivel Superior','Nivel Superior'),
    ('Nivel Medio','Nivel Medio'),
    ('Nivel Básico','Nivel Básico'),
)
Especialidades = (
    ('Ingeniero Telecomunicaciones','Ingeniero Telecomunicaciones'),
    ('Licenciado Mando Comunicaciones','Licenciado Mando Comunicaciones'),
    ('Técnico Medio Superior Comunicaciones','Técnico Medio Superior Comunicaciones'),
    ('Ingeniero Informático','Ingeniero Informática'),
    ('Ingeniero Ciber Seguridad','Ingeniero Ciber Seguridad'),
    ('Ingeniero Automático','Ingeniero Automático'), 
    ('Otro','Otro'),
)

class Oficial(models.Model):
    
    nombre=models.CharField(max_length=30,blank=True,null=False)
    apellido=models.CharField(max_length=30, verbose_name="Primer Apellido",blank=True,null=False)
    apellido2=models.CharField(max_length=30, verbose_name="Segundo Apellido",blank=True,null=False)
    grado=models.CharField(max_length=50,choices=Choices,blank=True,null=False)
    cargo=models.CharField(max_length=50,choices=Options,blank=True,null=False)
    
    CI = models.CharField( null=True, blank=False, max_length=11, unique=True,validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='El número de cédula debe tener 6 dígitos.'
            )
        ] )
    graduadoDe=models.CharField(max_length=50,choices=Especialidades,blank=False,null=True)
    escuelaProcedencia=models.CharField(max_length=50,choices=Escuelas,blank=False,null=True)
    nivel = models.CharField(max_length=50,choices=Niveles,null=True,blank=False)
    
    telefono = models.BigIntegerField(null=True, blank=True, verbose_name="Número de teléfono",validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message='El número debe tener 8 dígitos.'
            )
        ] )
    correo=models.EmailField(null=True,blank=True)
    direccion=models.CharField(max_length=100,null=True,blank=True)
    fecha_nacimiento=models.DateField(null=True,blank=False,verbose_name="Fecha de Nacimiento ")
    
    def __str__(self):
        return self.nombre + " " + self.apellido
    
    
class Postgrado(models.Model):
     user=models.ForeignKey(Oficial,on_delete=models.CASCADE)
     nombre=models.CharField(max_length=100)
     
     def __str__(self):
        return " Postgrado de "+ self.user.nombre +" "+ self.user.apellido + " : " + self.nombre