# -*- coding: utf-8 -*-
from odoo import fields, models, _


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    def get_required_field(self):
        req_fields = super(SubscriptionRequest, self).get_required_field()[:]
        req_fields.remove('iban')

        return req_fields
