from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    @api.model
    def create(self, values):
        # Llamada al método padre para la creación de la actividad
        res = super().create(values)
        # Actualiza la próxima actividad en el lead relacionado si corresponde
        res._set_next_activity_from_crm_in_partner()
        return res

    def _action_done(self, feedback=False, attachment_ids=None):
        # Actualiza la última actividad en el lead relacionado si corresponde
        self._set_last_activity_from_crm_in_partner()
        return super()._action_done(feedback=feedback, attachment_ids=attachment_ids)

    def _set_last_activity_from_crm_in_partner(self):
        # Iterar sobre las actividades para actualizar la última actividad en los leads relacionados
        for activity in self:
            if activity.res_model == "crm.lead":
                lead = self.env["crm.lead"].browse(activity.res_id)
                lead.set_last_activity_info(activity.activity_type_id.name)

    def _set_next_activity_from_crm_in_partner(self):
        # Iterar sobre las actividades para actualizar la próxima actividad en los leads relacionados
        for activity in self:
            if activity.res_model == "crm.lead":
                lead = self.env["crm.lead"].browse(activity.res_id)
                lead.set_next_activity(activity)
