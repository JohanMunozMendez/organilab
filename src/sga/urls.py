"""
@organization: Solvo
@license: GNU General Public License v3.0
@date: Created on 13 sept. 2018
"""

# Import functions of another modules
from django.urls import path, re_path

from .views import index_sga, template, editor, render_pdf_view

from django.conf.urls import  include
from . import views

# SGA
app_name = 'sga'

# Views
urlpatterns = [
    # sga/index_sga/
    path('index_sga', index_sga, name='index_sga'),
    path('barcode/<str:code>/', views.get_barcode_from_number, name='barcode_from_number'),
    path('label_editor_builder/<str:organilabcontext>/<int:org_pk>', template, name='template'),
    # sga/editor
    re_path(r'editor/(?P<organilabcontext>\w+)/(?P<org_pk>\d+)$', editor, name='editor'),
    re_path(r'get_preview/(?P<organilabcontext>\w+)/(?P<pk>\d+)$', views.get_preview, name='get_preview'),
    re_path(r'get_svgexport/(?P<is_pdf>\d+)/(?P<pk>\d+)$', views.get_svgexport, name='get_svgexport'),

    re_path(r'download/', render_pdf_view, name='download'),
    # sga/prudence
    path('prudence/<str:organilabcontext>', views.get_prudence_advice, name='prudence'),
    # sga/get_danger_indication
    path('danger/<str:organilabcontext>', views.get_danger_indication, name='get_danger_indication'),
    # sga/get_get_templateList
    re_path(r'add_personal/(?P<organilabcontext>\w+)/(?P<org_pk>\d+)$', views.create_personal_template, name='add_personal'),
    re_path(r'edit_personal/(?P<organilabcontext>\w+)/(?P<pk>\d+)$', views.edit_personal_template, name='edit_personal'),

    re_path(r'delete_sgalabel/(?P<organilabcontext>\w+)/(?P<org_pk>\d+)/(?P<pk>\d+)$', views.delete_sgalabel, name='delete_sgalabel'),
    re_path(r'add_substance/(?P<organilabcontext>\w+)', views.create_substance, name='add_substance'),
    re_path(r'add_recipient_size', views.create_recipient, name='add_recipient_size'),
    re_path(r'get_pictograms', views.get_pictograms, name='pictograms_list'),
    re_path(r'add_pictogram', views.add_pictogram, name='add_pictograms'),
    re_path(r'update_pictogram/(?P<id_pictogram>\w+)', views.update_pictogram, name='update_pictogram'),
    re_path(r'company/list/(?P<org_pk>\d+)', views.get_companies, name='get_companies'),
    re_path(r'company/add/(?P<org_pk>\d+)', views.create_company, name='add_company'),
    re_path(r'company/edit/(?P<org_pk>\d+)/(?P<pk>\d+)$', views.edit_company, name='edit_company'),
    re_path(r'company/remove/(?P<pk>\d+)$', views.remove_company, name='remove_company'),


    path('sgalabel/get_company/<int:pk>', views.get_company, name='get_company'),
    path('sgalabel/get_recipient_size/<str:organilabcontext>/<int:pk>', views.get_recipient_size, name='get_recipient_size'),
    path('sgalabel/get_sgacomplement_by_substance/<int:pk>', views.get_sgacomplement_by_substance, name='get_sgacomplement_by_substance'),
    path('sgalabel/create/<str:organilabcontext>/<int:org_pk>', views.create_sgalabel, name='sgalabel_create'),
    path('sgalabel/step_one/<str:organilabcontext>/<int:org_pk>/<int:pk>', views.sgalabel_step_one, name='sgalabel_step_one'),
    path('sgalabel/step_two/<str:organilabcontext>/<int:org_pk>/<int:pk>', views.sgalabel_step_two, name='sgalabel_step_two'),

]