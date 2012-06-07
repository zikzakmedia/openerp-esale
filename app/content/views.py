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
from content.models import *

import os

_('Add Content')
_('Results')
_('No results found.')
_('Author')
_('Search In')

def content_detail(request, content):
    """Content Detail"""
    kwargs = {
        'slug_'+get_language(): content, #slug is unique
    }
    if not request.user.is_staff:
        kwargs['status'] = True
    content = get_object_or_404(Content, **kwargs) #Content
    title = content.name
    metakeywords = content.metakey
    metadescription = content.metadesc
    tpl = content.template or 'default.html'
    if content.template is not 'default.html':
        if not os.path.exists(TEMPLATE_DIRS[0]+'/content/'+tpl):
            tpl = 'default.html'
    change_content = request.user.has_perm('content.change_content')

    return render_to_response("content/"+tpl, {'title':title,'metakeywords':metakeywords,'metadescription':metadescription,'content':content,'url':LIVE_URL,'change_content':change_content}, context_instance=RequestContext(request))

"""
Content Form. Add/Edit
"""
class ContentForm(ModelForm):
    class Meta:
        model = Content
        
@login_required
def content_form(request, content_id):
    """
    Content Form
    """
    form = ''
    redirect = ''
    context_instance=RequestContext(request)

    if request.method == 'POST':
        if content_id:
            content= Content.objects.get(id=content_id)
            form = ContentForm(request.POST, instance=content)
        else:
            form = ContentForm(request.POST)

        if form.is_valid():
            content = form.save(commit=False)
            
            if not content.id:
                content.created_by = request.user
            content.updated_by = request.user

            content.save()

        if LOCALE_URI:
            redirect = '%s/%s' % (context_instance['LOCALE_URI'], content.slug)
        else:
            redirect =  '/%s' % (content.slug)
    else:
        if content_id:
            content = get_object_or_404(Content,id=content_id)
            form = ContentForm(instance=content)
        else:
            form = ContentForm()
    return form, redirect

@login_required
def content_add(request):
    """
    Content Add
    """
    content = False
    context_instance=RequestContext(request)
    
    if not request.user.has_perm('content.add_content'):
        raise Http404
    form, redirect = content_form(request, content)
    if redirect:
        return HttpResponseRedirect(redirect)

    if LOCALE_URI:
        url_form = '%s/content/add/' % (context_instance['LOCALE_URI'])
    else:
        url_form =  '/content/add/'
                
    return render_to_response('content/form.html', {'form':form,'url_form':url_form,'title':_('Add Content')}, context_instance=RequestContext(request))

@login_required
def content_edit(request, content_id):
    """
    Content Edit
    """
    context_instance=RequestContext(request)

    if not request.user.has_perm('content.change_content'):
        raise Http404

    try:
        content_id = int(content_id)
    except ValueError:
        raise Http404

    form, redirect = content_form(request, content_id)
    if redirect:
        return HttpResponseRedirect(redirect)

    if LOCALE_URI:
        url_form = '%s/content/edit/%s' % (context_instance['LOCALE_URI'], content_id)
    else:
        url_form =  '/content/edit/%s' % (content_id)

    return render_to_response('content/form.html', {'form':form,'url_form':url_form,'title':_('Edit Content')}, context_instance=RequestContext(request))
