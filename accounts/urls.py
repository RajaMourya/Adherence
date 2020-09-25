

from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('plogin/',views.plogin,name = 'plogin'),
    path('pcreate/',views.pcreate,name = 'pcreate'),
    path('plogincheck/',views.plogincheck,name = 'plogincheck'),
    path('plogout/',views.plogout,name = 'plogout'),
    path('pcreatecheck/',views.pcreatecheck,name = 'pcreatecheck'),
    path('patient/',views.patient,name = 'patient'),
    path('predict/',views.predict,name = 'predict'),
    path('createpatient/',views.createpatient,name="createpatient"),
    path('details/<int:pat_id>',views.details,name='details'),
    path('search/',views.search,name = "search"),
]