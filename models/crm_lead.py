from odoo import api, fields, models


class Lead(models.Model):
    _inherit = "crm.lead"

    last_activity_date = fields.Date(
        readonly=True,
    )
    last_activity_type_name = fields.Char(
        readonly=True,
    )
    next_activity_id = fields.Many2one(
        comodel_name="mail.activity",
        readonly=True,
    )

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        res._set_last_crm_id_in_partner()
        return res

    def _set_last_crm_id_in_partner(self):
        for lead in self:
            lead.partner_id.last_crm_lead_id = lead.id

    def set_last_activity_info(self, activity_type_name):
        self.last_activity_date = fields.Date.today()
        self.last_activity_type_name = activity_type_name

    def set_next_activity(self, activity):
        self.next_activity_id = activity
