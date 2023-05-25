from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from djgentelella.views.select2autocomplete import BaseSelect2View, GPaginator
from djgentelella.groute import register_lookups
from rest_framework.response import Response

from auth_and_perms.api.serializers import ValidateUserAccessOrgLabSerializer
from auth_and_perms.organization_utils import user_is_allowed_on_organization, organization_can_change_laboratory
from laboratory.forms import ValidateShelfForm, ValidateShelfUnitForm
from laboratory.models import Object, OrganizationStructure, Catalog, Shelf, Provider
from auth_and_perms.models import Rol
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from laboratory.utils import get_pk_org_ancestors

class GPaginatorMoreElements(GPaginator):
    page_size = 100


@register_lookups(prefix="rol", basename="rolsearch")
class RolGModelLookup(BaseSelect2View):
    model = Rol
    fields = ['name']

@register_lookups(prefix="object", basename="objectsearch")
class ObjectGModelLookup(BaseSelect2View):
    model = Object
    fields = ['code', 'name']


@register_lookups(prefix="objectorgsearch", basename="objectorgsearch")
class ObjectGModelLookup(generics.RetrieveAPIView, BaseSelect2View):
    model = Object
    fields = ['code', 'name']
    org_pk = None
    shelf = None
    shelfobjet_type=None
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.shelf and self.shelf.limit_only_objects and self.shelfobjet_type:
            return self.shelf.available_objects_when_limit.filter(type=self.shelfobjet_type)

        queryset = super().get_queryset()

        if self.org_pk and self.shelfobjet_type:
            organizations = get_pk_org_ancestors(self.org_pk.pk)
            queryset = queryset.filter(organization__in=organizations,type=self.shelfobjet_type)
        else:
            queryset = queryset.none()
        return queryset

    def retrieve(self, request, pk, **kwargs):

        self.org_pk=get_object_or_404(OrganizationStructure.objects.using(settings.READONLY_DATABASE), pk=pk)
        user_is_allowed_on_organization(request.user, self.org_pk)
        form = ValidateShelfForm(request.GET)
        if form.is_valid():
            shelf = form.cleaned_data['shelf']
            if organization_can_change_laboratory(shelf.furniture.labroom.laboratory, self.org_pk):
                self.shelf=shelf
                self.shelfobjet_type=form.cleaned_data['objecttype']

        return self.list(request, pk, **kwargs)



@register_lookups(prefix="userbase", basename="userbase")
class User(BaseSelect2View):
    model = User
    fields = ['username']
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


@register_lookups(prefix="catalogunit", basename="catalogunit")
class CatalogUnitLookup(generics.RetrieveAPIView, BaseSelect2View):
    model = Catalog
    fields = ['description']
    shelf = None
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(key="units")
        if self.shelf:
            if self.shelf.measurement_unit:
                return queryset.filter(pk=self.shelf.measurement_unit.pk)
            else:
                return queryset
        else:
            return queryset.none()
        return queryset

    def retrieve(self, request, pk, **kwargs):

        self.org_pk=get_object_or_404(OrganizationStructure.objects.using(settings.READONLY_DATABASE), pk=pk)
        user_is_allowed_on_organization(request.user, self.org_pk)
        form = ValidateShelfUnitForm(request.GET)
        if form.is_valid():
            shelf = form.cleaned_data['shelf']
            self.shelf=shelf

        return self.list(request, pk, **kwargs)

@register_lookups(prefix="recipientsearch", basename="recipientsearch")
class RecipientModelLookup(generics.RetrieveAPIView, BaseSelect2View):
    model = Object
    fields = ['code', 'name']
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.org_pk:
            organizations = get_pk_org_ancestors(self.org_pk.pk)
            queryset = queryset.filter(organization__in=organizations,type=1)
        else:
            queryset = queryset.none()
        return queryset

    def retrieve(self, request, pk, **kwargs):

        self.org_pk=get_object_or_404(OrganizationStructure.objects.using(settings.READONLY_DATABASE), pk=pk)
        user_is_allowed_on_organization(request.user, self.org_pk)

        return self.list(request, pk, **kwargs)

@register_lookups(prefix="shelfobject_status_search", basename="shelfobject_status_search")
class ShelfObject_StatusModelLookup(generics.RetrieveAPIView, BaseSelect2View):
    model = Catalog
    fields = ['description']
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(key='shelfobject_status')
        return queryset

    def retrieve(self, request, pk, **kwargs):

        self.org_pk=get_object_or_404(OrganizationStructure.objects.using(settings.READONLY_DATABASE), pk=pk)
        user_is_allowed_on_organization(request.user, self.org_pk)

        return self.list(request, pk, **kwargs)


@register_lookups(prefix="provider", basename="provider")
class ProviderLookup(generics.RetrieveAPIView, BaseSelect2View):
    model = Provider
    fields = ['name']
    ordering = ['name']
    pagination_class = GPaginatorMoreElements
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    laboratory, serializer = None, None

    def get_queryset(self):
        queryset = super().get_queryset()
        result = queryset.none()
        if self.laboratory:
            result = queryset.filter(laboratory=self.laboratory)
        return result

    def list(self, request, *args, **kwargs):
        self.serializer = ValidateUserAccessOrgLabSerializer(data=request.GET, context={'user': request.user})

        if self.serializer.is_valid():
            self.laboratory = self.serializer.validated_data['laboratory']
            return super().list(request, *args, **kwargs)

        return Response({
                'status': 'Bad request',
                'errors': self.serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)