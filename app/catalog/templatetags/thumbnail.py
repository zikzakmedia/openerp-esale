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

from django import template
from django.template import Library, Node
from settings import *

import os
import cStringIO # *much* faster than StringIO
import urllib
import Image

register = template.Library()

class ThumbnailNode(Node):
    def __init__(self, source_var, size, default):
        self.source_var = source_var
        self.size = size
        self.default = '/static/images/%s/%s' % (BASE_TEMPLATE, default)
 
    def render(self, context):
        try:
            fileimage = template.Variable(self.source_var).resolve(context)
        except:
            fileimage = str(self.source_var)[1:-1]

        size = str(self.size)

        try:
            fname = fileimage.split('/')[-1:]
            fname = fname[0].split('.')
            size = size.split('x')
            base_image = '%s/%s/%s.%s' % (MEDIA_ROOT, 'catalog', fname[0], fname[1])
            thumb_image = '%s/%s/%sx%s/%s.%s' % (MEDIA_ROOT, 'catalog', size[0], size[1], fname[0], fname[1])

            #check thumb exist
            if not os.path.exists('%s/%s/%sx%s/%s.%s' % (MEDIA_ROOT, 'catalog', size[0], size[1], fname[0], fname[1])):
                #check if dir exist
                directory = "%s/%s/%sx%s" % (MEDIA_ROOT, 'catalog',size[0], size[1])
                if not os.path.exists(directory):
                    os.makedirs(directory)
                #check base image exist
                if not os.path.exists(base_image):
                    file = urllib.urlopen(fileimage)
                    im = cStringIO.StringIO(file.read()) # constructs a StringIO holding the image
                    img = Image.open(im)
                    # print img.format, img.size, img.mode
                    img.save(base_image)
                image = Image.open(base_image)
                image.thumbnail([int(size[0]), int(size[1])], Image.ANTIALIAS)
                image.save(thumb_image, image.format)
            filename = '%s%s/%sx%s/%s.%s' % (MEDIA_URL, 'catalog', size[0], size[1], fname[0], fname[1])
        except:
            filename = self.default

        return filename

def thumbnail(parser, token):
    """
    Creates a thumbnail image file.

    Basic tag Syntax::
        {% thumbnail [source] [size] [base image]%}

    *source* must be a ``File`` object: 'http://domain/file.png'

    *size* the size in the format ``[width]x[height]`` For example,
      ``{% thumbnail 'http://domain/file.png' 100x50 %}``

    *img_default* image name default. For example,
      ``{% thumbnail 'http://domain/file.png' 100x50 product_thumb.png %}``

    Demo:
      {% thumbnail 'http://domain/file.png' 100x50 product_thumb.png %}
      {% thumbnail value.base_image.filename 150x150 product_thumb.png %}

    Thumbnail image is created in MEDIA_ROOT/catalog directory. Thumbnail create directory size, for example, MEDIA_ROOT/50x50
    """

    parts = token.split_contents()

    if len(parts) < 3:
        raise template.TemplateSyntaxError("'thumbnail' tag must be of the form:  {% thumbnail [source] [size] [base image]%}")

    return ThumbnailNode(parts[1], parts[2], parts[3])

register.tag(thumbnail)
