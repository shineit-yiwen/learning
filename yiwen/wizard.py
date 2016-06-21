from openerp import models, fields, api

class Wizard(models.TransientModel):
    _name = 'yiwen.wizard'

    def _default_session(self):
        return self.env['yiwen.session'].browse(self._context.get('active_id'))

    session_id = fields.Many2one('yiwen.session',     
    	string="Session", required=True, default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")


    @api.multi
    def subscribe(self):
    	self.session_id.attendee_ids |= self.attendee_ids
        # self.session_id.attendee_ids = self.session_id.attendee_ids | self.attendee_ids
        # for session in self.session_id:
        #     session.attendee_ids |= self.attendee_ids
    	return {}