from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    last_crm_lead_id = fields.Many2one(
        comodel_name="crm.lead",
        readonly=True,
    )
    last_crm_lead_datetime = fields.Datetime(
        string="Last Opportunity Date",
        related="last_crm_lead_id.create_date",
        store=True,
    )
    last_crm_lead_date = fields.Date(
        compute="_compute_last_crm_lead_date",
        store=True,
        string="Last Opportunity",
    )

    last_activity_date = fields.Date(
        string="Last Activity",
    )
    last_activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type",
        string="Last Activity Type",
    )
    next_crm_activity_id = fields.Many2one(
        comodel_name="mail.activity",
        string="Next CRM Activity",
    )
    next_activity_date = fields.Date(
        string="Next Activity",
        related="next_crm_activity_id.date_deadline",
        store=True,
    )
    next_activity_activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type",
        string="Next Activity Type",
        related="next_crm_activity_id.activity_type_id",
        store=True,
    )

    @api.depends("last_crm_lead_datetime")
    def _compute_last_crm_lead_date(self):
        for partner in self:
            partner.last_crm_lead_date = partner.last_crm_lead_datetime
