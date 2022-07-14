from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    @api.model
    def create(self, values):
        res = super().create(values)
        res._set_next_activity_from_crm_in_partner()
        return res

    def _action_done(self, feedback=False, attachment_ids=None):
        self._set_last_activity_from_crm_in_partner()
        return super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

    def _set_last_activity_from_crm_in_partner(self):
        for activity in self:
            if activity.res_model != "crm.lead":
                continue
            lead = self.env["crm.lead"].browse(activity.res_id)
            lead.set_last_activity_info(activity.activity_type_id.name)

    def _set_next_activity_from_crm_in_partner(self):
        for activity in self:
            if activity.res_model != "crm.lead":
                continue
            lead = self.env["crm.lead"].browse(activity.res_id)
            lead.set_next_activity(activity)
