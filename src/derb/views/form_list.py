from django.contrib.admin.models import DELETION
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView

from derb.models import CustomForm
from laboratory.utils import organilab_logentry


@method_decorator(permission_required('derb.view_customform'), name='dispatch')
class FormList(ListView):
    model = CustomForm
    context_object_name = "forms"
    template_name = 'formBuilder/form_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['forms'] = CustomForm.objects.all()
        return context

@method_decorator(permission_required('derb.delete_customform'), name='dispatch')
class DeleteForm(DeleteView):
    model = CustomForm
    success_url = reverse_lazy('derb:form_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        ct = ContentType.objects.get_for_model(self.object)
        organilab_logentry(self.request.user, ct, self.object, DELETION, 'custom form')
        self.object.delete()
        return HttpResponseRedirect(success_url)

    # decir este formulario tiene x respuestas en el warning
@permission_required('derb.add_customform')
def CreateForm(request):

    if request.method == 'POST':

        empty_schema = {
            "name": request.POST.get('name'),
            "status": "admin",
            "components": []
        }

        custom_form = CustomForm.objects.create(
            name=empty_schema['name'],
            status=empty_schema['status'],
            schema=empty_schema
        )
        url = reverse('derb:edit_view', args=[custom_form.id])
        return JsonResponse({"url": url})
