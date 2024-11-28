from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    last_activity_date = fields.Date(
        string="Last Activity Date",
        readonly=True,
    )
    last_activity_type_name = fields.Char(
        string="Last Activity Type",
        readonly=True,
    )
    next_activity_id = fields.Many2one(
        comodel_name="mail.activity",
        string="Next Activity",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals):
        # Llamada al método `super` para respetar la lógica de creación existente
        leads = super().create(vals)
        leads._set_last_crm_id_in_partner()
        return leads

    def _set_last_crm_id_in_partner(self):
        for lead in self:
            if lead.partner_id:
                lead.partner_id.last_crm_lead_id = lead.id

    def set_last_activity_info(self, activity_type_name):
        # Actualizar la información de la última actividad
        self.write(
            {
                "last_activity_date": fields.Date.today(),
                "last_activity_type_name": activity_type_name,
            }
        )

    def set_next_activity(self, activity):
        # Establecer la próxima actividad para el lead
        self.next_activity_id = activity
