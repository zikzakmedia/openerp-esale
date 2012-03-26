# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2011 Zikzakmedia S.L. (http://zikzakmedia.com) All Rights Reserved.
#                       Raimon Esteve <resteve@zikzakmedia.com>
#                       Jesus Martín <jmartin@zikzakmedia.com>
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv, fields
from tools.translate import _

import unicodedata
import re
import netsvc

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

class product_category(osv.osv):
    _inherit = "product.category"

    def collect_children(self, category, children=None):
        if children is None:
            children = []

        for child in category.child_id:
            children.append(child.id)
            self.collect_children(child, children)

        return children

    def _get_recursive_cat_children_ids(self, cr, uid, ids, name, args, context=None):
        res = {}
        for category in self.browse(cr, uid, ids):
            res[category.id] = self.collect_children(category, [category.id])
        return res

    def onchange_name(self, cr, uid, ids, name, slug):
        value = {}
        if not slug:
            slug = slugify(unicode(name,'UTF-8'))
            value = {'slug': slug}
        return {'value':value}

    _columns = {
        'recursive_childen_ids': fields.function(_get_recursive_cat_children_ids, method=True, type='one2many', relation="product.category", string='All Child Categories'),
        'slug': fields.char('Slug', size=128, translate=True,help='Atention! If you change slug, you need change manually all full slug childreen categories'),
        'fslug': fields.char('Full Slug', size=256, translate=True, readonly=True),
        'description': fields.text('Description', translate=True),
        'metadescription': fields.text('Meta Description', translate=True),
        'metakeyword': fields.text('Meta Keyword', translate=True),
        'metatitle': fields.char('Title', size=256, translate=True),
        'status': fields.boolean('Status'),
        'default_sort_by': fields.selection([
                    ('position', 'Position'),
                    ('name', 'Name'),
                    ('price', 'Price')
                    ], 'Default Product Listing Sort (Sort By)'),
    }

    _sql_constraints = [
        ('uniq_slug', 'unique(slug)', "Slug must be unique"),
    ]

    _defaults = {
        'status': True,
        'default_sort_by': lambda *a: 'position',
    }

    def set_fslug(self, cr, uid, ids, context=None):
        """Get all path slug
        Delete first parent category (root category)
        :return string
        """
        if not isinstance(ids,list):
            ids = [ids]

        reads = self.read(cr, uid, ids, ['slug','parent_id'], context=context)
        result = []
        parent_slug = ''
        name = ''

        for record in reads:
            slug = record['slug']
            if record['parent_id']:
                name = record['parent_id'][1]

        if name:
            names = name.split(' / ')
            for name in names:
                result.append(slugify(name))
            del result[:1] #delete first element = Primary category
            parent_slug = "/".join(result)

        return parent_slug

    def check_slug_exist(self, cr, uid, ids, slug, context=None):
        """Check if there are another category same slug
        Slug is identificator unique
        :return True or False
        """

        if not isinstance(ids,list):
            ids = [ids]

        categories = self.pool.get('product.category').search(cr, uid, [('slug','=',slug),('id','not in',ids)])

        if len(categories)>0:
            return True
        else:
            return False

    def create(self, cr, uid, vals, context=None):
        """Slug is unique. Validate
        fslug recalculated
        """
        if context is None:
            context = {}

        if 'slug' in vals:
            ids = None
            check_slug = self.check_slug_exist(cr, uid, ids, vals['slug'], context)
            if check_slug:
                raise osv.except_osv(_("Alert"), _("This Slug exists. Choose another slug"))

        id = super(product_category, self).create(cr, uid, vals, context)

        if 'slug' in vals:
            fslug = "%s/" % (vals['slug'])
            parent_slug  = self.set_fslug(cr, uid, [id], context)
            if parent_slug:
                fslug = "%s/%s/" % (parent_slug, vals['slug'])
            self.write(cr, uid, id, {'fslug':fslug})

        return id

    def write(self, cr, uid, ids, vals, context=None):
        """Slug is unique. Validate
        fslug recalculated
        """

        if 'slug' in vals:
            check_slug = self.check_slug_exist(cr, uid, ids, vals['slug'], context)
            if check_slug:
                raise osv.except_osv(_("Alert"), _("This Slug exists. Choose another slug"))
            else:
                vals['fslug'] = "%s/" % (vals['slug'])
                parent_slug  = self.set_fslug(cr, uid, ids, context)

                if parent_slug:
                    vals['fslug'] = "%s/%s/" % (parent_slug, vals['slug'])

        return super(product_category, self).write(cr, uid, ids, vals, context=context)

    def copy(self, cr, uid, id, default={}, context=None):
        """Slug and fslug are unique. Add -copy
        """

        category = self.browse(cr, uid, id, context=context)
        if not default:
            default = {}

        if category.slug:
            default = default.copy()
            slug = category.slug
            while self.search(cr, uid, [('slug','=',slug)]):
                slug += '-copy'
            default['slug'] = slug

            #rewrite full slug
            full_slug = category.fslug.split('/')
            del full_slug[-1] #delete /
            del full_slug[-1] #delete last item
            full_slug.append(slug)
            default['fslug'] = "/".join(full_slug)+'/'

        return super(product_category, self).copy(cr, uid, id, default, context=context)

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_("Alert"), _("To Unlink this category mark status is False"))

product_category()

class product_template(osv.osv):
    _inherit = "product.template"

    def onchange_name(self, cr, uid, ids, name, slug):
        value = {}
        if not slug:
            slug = slugify(unicode(name,'UTF-8'))
            value = {'slug': slug}
        return {'value':value}

    _columns = {
        'codes': fields.text('Codes'),
        'zoook_exportable':fields.boolean('Export to e-sale?', change_default=True, help="If check export e-sale, this product are available in your e-sale. If you need not publish this product (despublish), unmark Active field in e-sale tab"),
        'zoook_status':fields.boolean('Active', help="If check this, e-sale product are available and shop it"),
        'zoook_saleshop_ids': fields.many2many('sale.shop', 'zoook_sale_shop_rel', 'product_tmp_id', 'sale_shop_id', 'Websites', help='Select yours Sale Shops available this product'),
        'visibility': fields.selection([('all','All'),('search','Search'),('catalog','Catalog'),('none','None')], 'Visibility'),
        'slug': fields.char('Slug', size=256, translate=True),
        'shortdescription': fields.text('Short Description', translate=True),
        'metadescription': fields.text('Description', translate=True),
        'metakeyword': fields.text('Keyword', translate=True),
        'metatitle': fields.char('Title', size=256, translate=True),
        'product_related_ids': fields.many2many('product.template', 'product_template_related_rel', 'product_id', 'product_related_id','Related Products'),
        'product_upsells_ids': fields.many2many('product.template', 'product_template_upsells_rel', 'product_id', 'product_upsells_id', 'Up-sells'),
        'product_crosssells_ids': fields.many2many('product.template', 'product_template_crosssells_rel', 'product_id', 'product_crosssells_id', 'Cross-sells'),
        'zoook_sequence': fields.integer('Sequence', help="Gives the sequence order when displaying category list."),
    }

    _defaults = {
        'zoook_status':lambda * a:True,
        'visibility': 'all',
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if 'slug' in vals and vals['slug']:
            if vals.get('zoook_exportable', False):
                #Set user's current lang.
                context['lang'] = self.pool.get('res.users').browse(cr, uid, uid).context_lang
                products = self.pool.get('product.template').search(cr, uid, [('slug','=',vals['slug'])], context=context)
                if len(products) > 0:
                    raise osv.except_osv(_("Alert"), _("This Slug exists. Choose another slug"))
                slug = vals['slug']
                if not isinstance(slug, unicode):
                    slug = unicode(slug,'UTF-8')
                slug = slugify(slug)
                vals['slug'] = slug

        return super(product_template, self).create(cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """Check slug if exists"""

        result = True
        if not isinstance(ids, list):
            ids = [ids]

        for id in ids:
            check_slug = False

            if vals.get('slug', False):
                check_slug = True
                slug = vals['slug']

            if vals.get('zoook_exportable', False):
                check_slug = True
                if 'slug' in vals:
                    slug =  vals['slug']
                else:
                    prod_template = self.pool.get('product.template').browse(cr, uid, id, context)
                    slug = prod_template.slug

            if check_slug:
                #Set user's current lang.
                #~ context['lang'] = self.pool.get('res.users').browse(cr, uid, uid).context_lang
                products = self.pool.get('product.template').search(cr, uid, [('slug','=',slug),('id','!=',id)], context=context)
                if len(products) > 0:
                    raise osv.except_osv(_("Alert"), _("Slug %s exists. Choose another slug") % (slug))

                slug = slugify(unicode(str(slug),'UTF-8'))
                vals['slug'] = slug

            result = result and super(product_template, self).write(cr, uid, [id], vals, context=context)

        return result

product_template()

class product_product(osv.osv):
    _inherit = "product.product"

    _columns = {
        'cartdescription': fields.char('Cart Description', size=256, translate=True),
    }

    def onchange_name(self, cr, uid, ids, name, slug):
        value = {}
        if not slug:
            slug = slugify(unicode(name,'UTF-8'))
            value = {'slug': slug}
        return {'value':value}

    def zoook_compute_price(self, cr, uid, shop_id, products, partner_id=None, context=None):
        if context is None:
            context = {}

        if partner_id is None:
            partner_id = []

        logger = netsvc.Logger()
    
        product_obj = self.pool.get('product.product')
        product_template_obj = self.pool.get('product.template')
        sale_shop_obj = self.pool.get('sale.shop')
        product_pricelist_obj = self.pool.get('product.pricelist')

        shop = sale_shop_obj.browse(cr, uid, shop_id)

        pricelist_id = self.pool.get('res.partner').browse(cr, uid, partner_id).property_product_pricelist.id
        if not pricelist_id:
            pricelist_id = shop.pricelist_id.id
            if not pricelist_id:
                logger.notifyChannel("Zoook", netsvc.LOG_WARNING, _("Not Price List available Partner or Shop."))
                return False

        pricelist = product_pricelist_obj.browse(cr, uid, pricelist_id)

        result = {}

        decimal = self.pool.get('decimal.precision').precision_get(cr, uid, 'Sale Price')
        for product in products:
            product_price = ''
            try:
                #~ Product Taxes is computed by product.product, not product.template.
                #~ Searh all product.product and get price less
                products = []
                prods = product_obj.search(cr, uid, [('product_tmpl_id','=',product['product_id'])])
                for prod in product_obj.browse(cr, uid, prods):
                    price = product_pricelist_obj.price_get(cr, uid, [pricelist_id], prod.id, 1.0)[pricelist_id]
                    if shop.special_price: #if this sale shop available Special Price
                        if prod.special_price != 0.0 and prod.special_price < price:
                            price = prod.special_price
                    products.append({'product_id': prod.id, 'price': price})
                products = sorted(products, key=lambda k: k['price'])

                if shop.zoook_tax_include:
                    product_template = product_template_obj.browse(cr, uid, product['product_id'])
                    price_compute_all = self.pool.get('account.tax').compute_all(cr, uid, product_template.taxes_id, products[0]['price'], product['quantity'], address_id=None, product=product_template, partner=None)

                    product_price = price_compute_all['total_included']
                else:
                    product_price = products[0]['price']
            finally:
                if product_price:
                    product_price = '%.*f' % (decimal, product_price) #decimal precision
                    result[str(product['product_id'])] = {"regularPrice": str(product_price)+' '+pricelist.currency_id.symbol} #{"1":{"regularPrice":"50 €"}

        return result

    def copy(self, cr, uid, id, default={}, context=None):
        product = self.read(cr, uid, id, ['slug'], context=context)
        if  product['slug']:
            default.update({
                'slug': product['slug']+ _('-copy'),
            })

        return super(product_product, self).copy(cr, uid, id, default, context)

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(_("Alert"), _("To Unlink this product mark status is False"))

product_product()
