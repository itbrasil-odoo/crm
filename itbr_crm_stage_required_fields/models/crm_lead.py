from odoo import models, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def write(self, vals):
        msg = _("Os seguintes campos são obrigatórios para a etapa %s:\n %s")
        # msg = _("The following fields are required for stage %s. %s")
        # separe os campos que faltam por linha e adione "-" antes field_description
        missing_fields = []
        if "stage_id" in vals:
            stage = self.env["crm.stage"].browse(vals["stage_id"])
            required_fields = stage.required_fields_ids
            for field in required_fields:
                if not self[field.name]:
                    missing_fields += ["\n- " + field.field_description]
            if missing_fields:
                raise ValidationError(msg % (stage.name, "".join(missing_fields)))
        return super().write(vals)
