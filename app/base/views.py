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
from django.http import HttpResponse, Http404
from django.utils.translation import get_language, ugettext as _
from django.contrib.auth.decorators import login_required

from itertools import chain

from settings import *
from base.models import *

import os
import magic

def ir_attachment_file(request, file):
    """Document File
    Download document (file)
    - file url = document
    :param request
    :param file
    :return HttpResponse
    """

    kwargs = {
        'store_fslug': file,
        'visibility__in': ['public'],
    }

    if request.user.username:
        kwargs['visibility__in'] = ['public','register']

    attachment = get_object_or_404(IrAttachment, **kwargs)

    file = str(unicode(attachment.res_name).encode('utf-8'))
    doc = '%(root)s%(file)s' % {'root':ATTACHMENT_ROOT,'file':attachment.store_fname}

    try:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(doc)
        image_data = open(doc, "rb").read()
    except:
        raise Http404

    response = HttpResponse(image_data, mimetype=mime_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % (attachment.datas_fname)
    return response
