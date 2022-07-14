from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    last_crm_lead_id = fields.Many2one(
        comodel_name="crm.lead",
        readonly=True,
    )
    last_crm_lead_datetime = fields.Datetime(
        related="last_crm_lead_id.create_date",
        string="Last Opportunity",
    )
    last_crm_lead_date = fields.Date(
        compute="_compute_last_crm_lead_date",
        store=True,
    )
    last_activity_date = fields.Date(
        related="last_crm_lead_id.last_activity_date",
        string="Last Activity",
        store=True,
    )
    last_activity_type_name = fields.Char(
        related="last_crm_lead_id.last_activity_type_name",
        string="Type Activity",
        store=True,
    )
    next_activity_id = fields.Many2one(
        related="last_crm_lead_id.next_activity_id",
    )
    next_activity_date = fields.Date(
        related="next_activity_id.date_deadline",
        string="Next Activity",
        store=True,
    )
    next_activity_type_name = fields.Char(
        related="next_activity_id.activity_type_id.name",
        string="Type Activity",
        store=True,
    )

    @api.depends("last_crm_lead_datetime")
    def _compute_last_crm_lead_date(self):
        for partner in self:
            partner.last_crm_lead_date = partner.last_crm_lead_datetime
