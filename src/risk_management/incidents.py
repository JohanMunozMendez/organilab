import django_excel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator

from laboratory.decorators import user_group_perms
from laboratory.views import djgeneric
from risk_management.forms import IncidentReportForm
from risk_management.models import IncidentReport
from weasyprint import HTML
from django.utils.translation import ugettext as _


@method_decorator(login_required, name='dispatch')
@method_decorator(user_group_perms(perm='risk_management.view_incidentreport'), name='dispatch')
class IncidentReportList(djgeneric.ListView):
    model = IncidentReport
    ordering = 'pk'
    ordering = ['incident_date' ]
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            queryset = queryset.filter(short_description__icontains=q)
        return queryset


    def get_context_data(self, **kwargs):
        context = super(IncidentReportList, self).get_context_data()
        q = self.request.GET.get('q', '')

        context['q'] = q
        if q:
            context['pgparams'] = '?q=%s&'%(q,)
        else:
            context['pgparams'] = '?'
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(user_group_perms(perm='risk_management.add_incidentreport'), name='dispatch')
class IncidentReportCreate(djgeneric.CreateView):
    model = IncidentReport
    form_class = IncidentReportForm
    success_url = reverse_lazy('riskmanagement:riskzone_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['initial']={
            'laboratories':[self.lab]
        }
        return kwargs
@method_decorator(login_required, name='dispatch')
@method_decorator(user_group_perms(perm='risk_management.change_incidentreport'), name='dispatch')
class IncidentReportEdit(djgeneric.UpdateView):
    model = IncidentReport
    form_class = IncidentReportForm
    success_url = reverse_lazy('riskmanagement:riskzone_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['initial']={
            'laboratories':[self.lab]
        }
        return kwargs
@method_decorator(login_required, name='dispatch')
@method_decorator(user_group_perms(perm='risk_management.delete_incidentreport'), name='dispatch')
class IncidentReportDelete(djgeneric.DeleteView):
    model = IncidentReport
    success_url = reverse_lazy('riskmanagement:riskzone_list')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_group_perms(perm='risk_management.view_incidentreport'), name='dispatch')
class IncidentReportDetail(djgeneric.DetailView):
    model = IncidentReport

def make_book_incidentreport(incidents):
    content = {}
    funobjs = [
        [
_('Identificador'),
_('Creation Date'),
_('Short Description'),
_('Incident Date'),
_('Causes'),
_('Infraestructure impact'),
_('People impact'),
_('Environment impact'),
_('Result of plans'),
_('Mitigation actions'),
_('Recomendations'),
_('Laboratories'),
         ]
    ]
    for obj in incidents:
       funobjs.append([
           obj.id,
           str(obj.creation_date),
           obj.short_description,
           obj.incident_date,
           obj.causes,
           obj.infraestructure_impact,
           obj.people_impact,
           obj.environment_impact,
           obj.result_of_plans,
           obj.mitigation_actions,
           obj.recomendations,
           ",".join([x.name for x in obj.laboratories.all()]),
            ])
    content[_('Incidents')] = funobjs

    return content



@login_required
@user_group_perms(perm='laboratory.do_report')
def report_incidentreport(request, *args, **kwargs):
    var = request.GET.get('pk', '')
    lab = kwargs.get('lab_pk')
    if var:
        incidentreport =  IncidentReport.objects.filter(pk=var)
    else:
        incidentreport = IncidentReport.objects.filter(laboratories__in=[lab])
    fileformat = request.GET.get('format', 'pdf')
    if fileformat in ['xls', 'xlsx', 'ods']:
        return django_excel.make_response_from_book_dict(
            make_book_incidentreport(incidentreport), fileformat, file_name="incident.%s" % (fileformat,))

    template = get_template('risk_management/incidentreport_pdf.html')

    context = {
        'object_list': incidentreport,
        'datetime': timezone.now(),
        'request': request,
        'laboratory': lab
    }

    html = template.render(
        context=context).encode("UTF-8")

    page = HTML(string=html, encoding='utf-8').write_pdf()

    response = HttpResponse(page, content_type='application/pdf')
    response[
        'Content-Disposition'] = 'attachment; filename="incident_report.pdf"'
    return response
