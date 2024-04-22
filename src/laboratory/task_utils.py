from django.db.models import Sum
from django.utils import timezone

from laboratory.models import Laboratory, InformsPeriod, Inform, PrecursorReportValues, \
    ShelfObject, ObjectLogChange


def create_informsperiods(informscheduler, now=timezone.now()):
    last_update = informscheduler.last_execution
    if last_update is not None:
        last_close = last_update.close_application_date
        next_update = last_update.start_application_date + timezone.timedelta(
            days=informscheduler.period_on_days)
    else:
        next_update = informscheduler.start_application_date
        last_close = informscheduler.close_application_date



    last_close = last_close + timezone.timedelta(days=informscheduler.period_on_days)
    if next_update == now.today().date():
        labs = Laboratory.objects.filter(organization__pk=informscheduler.organization.pk)
        ip=InformsPeriod.objects.create(
            scheduler=informscheduler,
            organization=informscheduler.organization,
            inform_template=informscheduler.inform_template,
            start_application_date=next_update,
            close_application_date=last_close

        )
        for lab in labs:
            inform = Inform.objects.create(
                organization=informscheduler.organization,
                name="%s -- %s"%(informscheduler.name, lab.name),
                custom_form=informscheduler.inform_template,
                context_object=lab,
                schema=informscheduler.inform_template.schema,
            )
            ip.informs.add(inform)


def save_object_report_precursor(report):
    lab = report.laboratory
    for precursor in ShelfObject.objects.filter(in_where_laboratory=lab,
                                                object__sustancecharacteristics__is_precursor=True):

        obj = PrecursorReportValues.objects.filter(precursor_report=report,
                                                object=precursor.object,
                                                measurement_unit= precursor.measurement_unit).first()

        if obj:
            add_quantity = precursor.quantity
            obj.quantity += add_quantity
            obj.save()
        else:

            object_list = ObjectLogChange.objects.filter(laboratory=lab, precursor=True,
                                                         object=precursor.object,
                                                         measurement_unit=precursor.measurement_unit,
                                                         update_time__month=report.month,
                                                         update_time__year=report.year)

            providers = [ol.provider for ol in object_list.filter(provider__isnull=False)]
            subject = [ol.subject for ol in object_list.filter(subject__isnull=False)]
            bills = [ol.bill for ol in object_list.filter(bill__isnull=False)]
            income = object_list.filter(type_action__in=[0,1]).aggregate(amount=Sum('diff_value', default=0))["amount"]
            PrecursorReportValues.objects.create(precursor_report=report,
                                                 object=precursor.object,
                                                 measurement_unit= precursor.measurement_unit,
                                                 quantity = precursor.quantity,
                                                 new_income = income,
                                                 bills = ", ".join(bills),
                                                 providers=", ".join(providers),
                                                 stock = precursor.quantity,
                                                 month_expense = abs(object_list.filter(type_action__in=[2,3]).aggregate(amount=Sum('diff_value', default=0))["amount"]),
                                                 final_balance = precursor.quantity,
                                                 reason_to_spend = ", ".join(subject)
                                                 )


def build_precursor_report_from_reports(first_report, second_report):
    if second_report:
        first_report = PrecursorReportValues.objects.filter(precursor_report= first_report)
        second_report = PrecursorReportValues.objects.filter(precursor_report= second_report)
        for obj in first_report:

            old_obj = second_report.filter(object=obj.object, measurement_unit=obj.measurement_unit).first()
            if old_obj:
                obj.previous_balance = old_obj.final_balance
                obj.stock = old_obj.final_balance+obj.new_income
                obj.final_balance = obj.stock-obj.month_expense
                obj.save()




