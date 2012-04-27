# -*- encoding: utf-8 -*-
############################################################################################
#
#    Zoook. OpenERP e-sale, e-commerce Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404 
from django.template import RequestContext
from django.utils.translation import get_language, ugettext as _
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from settings import *
from tools.cms.models import *

def modules_list(request):
    """
    Modules List
    """
    if not request.user.has_perm('cms.change_modules'):
        raise Http404

    modules = Modules.objects.filter().order_by('position')
    title = _('Modules')

    return render_to_response('cms/modules/list.html', {'title':title,'modules':modules}, context_instance=RequestContext(request))

class ModulesForm(ModelForm):
    """
    Modules Form. Add/Edit
    """

    class Meta:
        model = Modules
        
@login_required
def modules_form(request, modules_id):
    """
    Modules Form
    """
    form = ''
    redirect = ''
    context_instance=RequestContext(request)

    if request.method == 'POST':
        if modules_id:
            modules = Modules.objects.get(id=modules_id)
            form = ModulesForm(request.POST, instance=modules)
        else:
            form = ModulesForm(request.POST)
        if form.is_valid():
            modules = form.save()
            redirect = "%s/cms/modules/list/" % (context_instance['LOCALE_URI'])
            #~ return HttpResponseRedirect(redirect)
    else:
        if modules_id:
            modules = get_object_or_404(Modules,id=modules_id)
            form = ModulesForm(instance=modules)
        else:
            form = ModulesForm()
    return form, redirect

@login_required
def modules_add(request):
    """
    Modules Add
    """
    _('All Modules')
    modules = False
    context_instance=RequestContext(request)

    if not request.user.has_perm('cms.add_modules'):
        raise Http404
    form, redirect = modules_form(request, modules)
    if redirect:
        return HttpResponseRedirect(redirect)
    url_form = '%s/cms/modules/add/' % (context_instance['LOCALE_URI'])
    return render_to_response('cms/modules/form.html', {'form':form,'url_form':url_form,'title':_('Add modules')}, context_instance=RequestContext(request))

@login_required
def modules_edit(request, modules_id):
    """
    Modules Edit
    """
    context_instance=RequestContext(request)

    if not request.user.has_perm('cms.change_modules'):
        raise Http404

    try:
        content_id = int(modules_id)
    except ValueError:
        raise Http404

    form, redirect = modules_form(request, modules_id)
    if redirect:
        return HttpResponseRedirect(redirect)
    url_form = '%s/cms/modules/edit/%s' % (context_instance['LOCALE_URI'], modules_id)
    return render_to_response('cms/modules/form.html', {'form':form,'url_form':url_form,'title':_('Edit modules')}, context_instance=RequestContext(request))
