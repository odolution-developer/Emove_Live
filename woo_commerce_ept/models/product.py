# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_woo_product_count(self):
        woo_product_obj = self.env['woo.product.product.ept']
        for product in self:
            woo_products = woo_product_obj.sudo().search([('product_id', '=', product.id)])
            product.woo_product_count = len(woo_products) if woo_products else 0

    woo_product_count = fields.Integer(string='# Sales Count', compute='_compute_woo_product_count')
    image_url = fields.Char(size=600, string='Image URL')

    def write(self, vals):
        """
        This method use to archive/active woo product base on odoo product.
        @author: Maulik Barad on Date 21-May-2020.
        Migrated by Maulik Barad on Date 07-Oct-2021.
        """
        if 'active' in vals.keys():
            woo_product_product_obj = self.env['woo.product.product.ept']
            for product in self:
                woo_product = woo_product_product_obj.search([('product_id', '=', product.id)])
                if vals.get('active'):
                    woo_product = woo_product_product_obj.with_context(active_test=False).search(
                        [('product_id', '=', product.id), ('active', '=', False)])
                woo_product.write({'active': vals.get('active')})
        return super(ProductProduct, self).write(vals)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def write(self, vals):
        """
        This method use to archive/unarchive woo product templates base on odoo product templates.
        :parameter: self, vals
        :return: res
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 09/12/2019.
        :Task id: 158502
        Migrated by Maulik Barad on Date 07-Oct-2021.
        """
        if 'active' in vals.keys():
            woo_product_template_obj = self.env['woo.product.template.ept']
            for template in self:
                woo_templates = woo_product_template_obj.search([('product_tmpl_id', '=', template.id)])
                if vals.get('active'):
                    woo_templates = woo_product_template_obj.search([('product_tmpl_id', '=', template.id),
                                                                     ('active', '=', False)])
                woo_templates.write({'active': vals.get('active')})
        res = super(ProductTemplate, self).write(vals)
        return res

    def _compute_woo_template_count(self):
        """
        Migrated by Maulik Barad on Date 07-Oct-2021.
        """
        woo_product_template_obj = self.env['woo.product.template.ept']
        for template in self:
            woo_templates = woo_product_template_obj.sudo().search([('product_tmpl_id', '=', template.id)])
            template.woo_template_count = len(woo_templates) if woo_templates else 0

    woo_template_count = fields.Integer(string='# Sales', compute='_compute_woo_template_count')


class Pricelist(models.Model):
    _inherit = 'product.pricelist'

    def _get_applicable_rules(self, products, date, **kwargs):
        self and self.ensure_one()
        woo_products = self.env['woo.product.product.ept'].sudo().search([('product_id', 'in', products.ids)])
        if woo_products:
            return self.env['product.pricelist.item'].with_context(active_test=False).search(
                self._get_rules_domain_woo_ept(products=products, date=date, **kwargs)
            )
        return self.env['product.pricelist.item'].with_context(active_test=False).search(
            self._get_applicable_rules_domain(products=products, date=date, **kwargs)
        )

    def _get_rules_domain_woo_ept(self, products, date, **kwargs):
        self and self.ensure_one()
        if products._name == 'product.template':
            templates_domain = ('product_tmpl_id', 'in', products.ids)
            products_domain = ('product_id.product_tmpl_id', 'in', products.ids)
        else:
            templates_domain = ('product_tmpl_id', 'in', products.product_tmpl_id.ids)
            products_domain = ('product_id', 'in', products.ids)

        return [
            ('pricelist_id', '=', self.id),
            '|', ('categ_id', '=', False), ('categ_id', 'parent_of', products.categ_id.ids),
            '|', ('product_tmpl_id', '=', False), templates_domain,
            '|', ('product_id', '=', False), products_domain
        ]
