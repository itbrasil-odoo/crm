from odoo import models, fields

import logging

_logger = logging.getLogger(__name__)


class CrmStage(models.Model):
    _inherit = "crm.stage"

    required_fields_ids = fields.Many2many(
        "ir.model.fields",
        string="Required Fields",
        domain="[('model_id', '=', 'crm.lead')]",
    )
