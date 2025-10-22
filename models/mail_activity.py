from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    crm_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Related Partner",
        compute="_compute_crm_partner_id",
        store=True,
    )

    @api.depends("res_model", "res_id")
    def _compute_crm_partner_id(self):
        for activity in self:
            if activity.res_model != "crm.lead":
                activity.crm_partner_id = False
                continue
            lead = self.env["crm.lead"].browse(activity.res_id)
            activity.crm_partner_id = lead.partner_id

    @api.model_create_multi
    def create(self, values):
        res = super().create(values)
        res._set_next_activity_in_partner_if_needed()
        return res

    def _action_done(self, feedback=False, attachment_ids=None):
        self._set_last_activity_done_in_partner()
        return super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

    def _set_last_activity_done_in_partner(self):
        # When done, the activity is deleted
        for activity in self:
            if activity.res_model != "crm.lead":
                continue
            lead = self.env["crm.lead"].browse(activity.res_id)
            partner = lead.partner_id
            if not partner:
                continue
            today = fields.Date.today()
            if not partner.last_activity_date or today > partner.last_activity_date:
                partner.last_activity_date = today
                partner.last_activity_type_id = activity.activity_type_id
            next_activity = self.search(
                [
                    ("res_model", "=", "crm.lead"),
                    ("date_deadline", ">=", today),
                    ("crm_partner_id", "=", partner.id),
                    ("id", "!=", activity.id),
                ],
                order="date_deadline asc",
                limit=1,
            )
            partner.next_crm_activity_id = next_activity

    def _set_next_activity_in_partner_if_needed(self):
        for activity in self:
            if activity.res_model != "crm.lead":
                continue
            lead = self.env["crm.lead"].browse(activity.res_id)
            partner = lead.partner_id
            if not partner:
                continue
            if activity.date_deadline < fields.Date.today():
                continue
            if (
                not partner.next_activity_date
                or activity.date_deadline < partner.next_activity_date
            ):
                partner.next_crm_activity_id = activity


# Server action
# leads = env["crm.lead"].search([("partner_id", "!=", False)])
# partners = {}
# for lead in leads:
#     if not lead.message_ids.filtered(lambda m: m.mail_activity_type_id):
#         continue
#     latest_message = lead.message_ids.filtered(
#         lambda m: m.mail_activity_type_id
#     ).sorted(key=lambda m: m.date, reverse=True)[0]
#     if lead.partner_id.id not in partners:
#         partners[lead.partner_id.id] = (
#             latest_message.mail_activity_type_id,
#             latest_message.date,
#         )
#     if latest_message.date > partners[lead.partner_id.id][1]:
#         partners[lead.partner_id.id] = (
#             latest_message.mail_activity_type_id.id,
#             latest_message.date,
#         )

# for partner_id, (activity_type, date) in partners.items():
#     env["res.partner"].browse(partner_id).write(
#         {
#             "last_activity_date": date,
#             "last_activity_type_id": activity_type,
#         }
#     )

# crm_activities = env["mail.activity"].search([("res_model", "=", "crm.lead")])
# crm_activities._compute_crm_partner_id()
# crm_activities._set_next_activity_in_partner_if_needed()
