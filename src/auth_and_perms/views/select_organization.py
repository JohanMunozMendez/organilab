from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from auth_and_perms.node_tree import get_organization_tree
from laboratory.models import OrganizationStructure

@login_required
def select_organization_by_user(request, org_pk=None):
    query_list = OrganizationStructure.os_manager.filter_organization_by_user(request.user).distinct().order_by('-parent')
    parent_structure = list(query_list.order_by('level'))
    parents=query_list.filter(parent=None).values_list('pk', flat=True)
    nodes = []
    pks=[]
    for node in parent_structure:
        if node.pk not in pks:
            get_organization_tree(node, nodes, request.user, pks, level=0, parents=parents, append_info=False, extras={'active': True})

    context = {
        'nodes': nodes,
        'has_nodes': len(nodes)
    }

    return render(request, 'auth_and_perms/select_organization.html', context=context)
