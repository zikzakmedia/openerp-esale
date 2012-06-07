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

from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from tools.zoook import siteConfiguration
from tools.paginator import *
from blog.models import *
from settings import *

import os

def blog_list(request, key=False):
    """All Blog
    List all blog. Available with Pagination
    :param request
    :return render_to_response
    """

    site_configuration = siteConfiguration(SITE_ID)

    blogs = Blog.objects.all().order_by('-created_on')
    blogs = blogs.filter(status=True)
    if key:
        kwargs = {
            'metakey_'+get_language()+"__icontains": key,
        }
        query = Q(**kwargs)
        blogs = blogs.filter(query)

    num_pages = get_num_pages(blogs, PAGINATOR_BLOG_TOTAL)
    title = _('Blog :: All Posts %(key)s - Page %(page)s of %(total)s') % {
                            'key': key and key or '',
                            'page': int(request.GET.get('page', '1')),
                            'total': num_pages
                        }
    metadescription = _('List all post %(key)s blog of %(site)s. Page %(page)s of %(total)s') % {
                            'key': key and key or '',
                            'site':site_configuration.site_title, 
                            'page':int(request.GET.get('page', '1')),
                            'total':num_pages
                        }

    return render_to_response("blog/list.html", {
                            'title':title, 
                            'metadescription': metadescription,
                            'blogs': blogs
                        },
                        context_instance=RequestContext(request))

def blog_detail(request, blog):
    """Blog Detail
    Detail content blog
    :param request
    :param blog
    :return render_to_response
    """

    kwargs = {
        'slug_'+get_language(): blog, #slug is unique
    }
    if not request.user.is_staff:
        kwargs['status'] = True
    blog = get_object_or_404(Blog, **kwargs)

    title = blog.name
    metakeywords = blog.metakey
    metadescription = blog.metadesc
    
    tpl = blog.template or 'default.html'
    if blog.template is not 'default.html':
        if not os.path.exists(TEMPLATE_DIRS[0]+'/blog/'+tpl):
            tpl = 'default.html'

    change_blog = request.user.has_perm('blog.change_blog')

    values = {
        'title':title,
        'metakeywords':metakeywords,
        'metadescription':metadescription,
        'blog':blog,
        'twitter_user':TWITTER_USER,
        'url': LIVE_URL,
        'change_blog':change_blog,
    }

    return render_to_response("blog/"+tpl, values, context_instance=RequestContext(request))

"""
Blog Form. Add/Edit
"""
class BlogForm(ModelForm):
    class Meta:
        model = Blog

@login_required
def blog_form(request, blog_id):
    """
    Blog Form
    """
    form = ''
    redirect = ''
    context_instance=RequestContext(request)

    if request.method == 'POST':
        if blog_id:
            blog = Blog.objects.get(id=blog_id)
            form = BlogForm(request.POST, instance=blog)
        else:
            form = BlogForm(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)

            if not blog.id:
                blog.created_by = request.user
            blog.updated_by = request.user

            blog.save()

        if LOCALE_URI:
            redirect = "%s/blog/%s" % (context_instance['LOCALE_URI'], blog.slug)
        else:
            redirect = "/blog/%s" % (blog.slug)
    else:
        if blog_id:
            blog = get_object_or_404(Blog,id=blog_id)
            form = BlogForm(instance=blog)
        else:
            form = BlogForm()
    return form, redirect

@login_required
def blog_add(request):
    """
    Blog Add
    """
    _('Add Blog')
    blog = False
    context_instance=RequestContext(request)
    
    if not request.user.has_perm('blog.add_blog'):
        raise Http404
    form, redirect = blog_form(request, blog)
    if redirect:
        return HttpResponseRedirect(redirect)
        
    if LOCALE_URI:
        url_form = '%s/blog/add/' % (context_instance['LOCALE_URI'])
    else:
        url_form = '/blog/add/'

    return render_to_response('blog/form.html', {'form':form,'url_form':url_form,'title':_('Add blog')}, context_instance=RequestContext(request))

@login_required
def blog_edit(request, blog_id):
    """
    Blog Edit
    """
    context_instance=RequestContext(request)

    if not request.user.has_perm('blog.change_blog'):
        raise Http404

    try:
        content_id = int(blog_id)
    except ValueError:
        raise Http404

    form, redirect = blog_form(request, blog_id)
    if redirect:
        return HttpResponseRedirect(redirect)

    if LOCALE_URI:
        url_form = '%s/blog/edit/%s' % (context_instance['LOCALE_URI'], blog_id)
    else:
        url_form = '/blog/edit/%s' % (blog_id)

    return render_to_response('blog/form.html', {'form':form,'url_form':url_form,'title':_('Edit blog')}, context_instance=RequestContext(request))
