# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api, exceptions


class Course(models.Model):
	_name = 'yiwen.course'
	name = fields.Char(string = "Title",required = True)
	description = fields.Text()
	main = fields.Text()
	style = fields.Text()
	product_image = fields.Binary("Image")
	state = fields.Selection([
		('draft', "Draft"),
		('confirmed', "Confirmed"),
		('done', "Done"),],default = "draft")

	responsible_id = fields.Many2one("res.users",
		ondelete = "set null",string = "Responsible",index = True)
	session_ids = fields.One2many("yiwen.session","course_id",string = "Sessions")
	course_number = fields.One2many("material","details",string="课程数")

# 数据库约束：CHECK(name ! =  description表示name与description所输入的字符串不能相同。。。。
# UNIQUE(name)表示名字必须是唯一的
	_sql_constraints  =  [
        ('name_description_check',
         'CHECK(name ! =  description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]
	@api.multi
	def action_draft(self):
		self.state = 'draft'
	
	@api.multi
	def action_confirm(self):
		self.state = 'confirmed'
	
	@api.multi
	def action_done(self):
		self.state = 'done'

class material(models.Model):
	_name="material"
	material=fields.Text(string=" 主")
	inside=fields.Char()
	details=fields.Many2one("sample.list")

class School(models.Model):
	_name = 'yiwen.school'
	name = fields.Char(string = "School",required = "True")
	# attendee_ids = fields.Many2many("res.partner",string = "Attendees")
	telephone = fields.Integer()
	address = fields.Char()
	new_password = fields.Char(string = "Password")
	description = fields.Text()

class parnet_enhanced(models.Model):
	_inherit = 'res.partner'
	school_id = fields.Many2one("yiwen.school",string = "School")
	
class Session(models.Model):
	_name = 'yiwen.session'
	name = fields.Char(required = True)
	start_date = fields.Date(store = True)
	end_date = fields.Date(compute = "_get_end_date",inverse = "change_Duration")
	duration = fields.Float(digits = (6,2),help = "Duration in days")
	seats = fields.Integer(string = "Seats")
	attendee_ids = fields.Many2many("res.partner",string = "Attendees")
	# taken_seats  =  fields.Float(string = "Taken seats", compute = '_taken_seats')
	num_attendee = fields.Integer(compute = "get_attendee_ids")
	course_id = fields.Many2one("yiwen.course",
		ondelete = "cascade",string = "Course",required = "True")
	instructor_id = fields.Many2one("res.partner",string = "Instructor")
	school_id  =  fields.Many2one("yiwen.school", related = "instructor_id.school_id")
	# domain = ["|",("instructor"," = ",True),("category_id.name","ilike","school")]
	active  =  fields.Boolean(string = "Active",default = True)
	attendees_count = fields.Integer(string = "Attendees count",
		compute = "_get_attendees_count",store = True)

# 视图的状态：default = "draft表示默认为draft
	state  =  fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('done', "Done"),],default = "draft")
	@api.multi
	def action_draft(self):
		self.state  =  'draft'

	@api.multi
	def action_confirm(self):
		self.state  =  'confirmed'
	@api.multi
	def action_done(self):
		self.state  =  'done'

	@api.multi
	def action_unconfirm(self):
		raise exceptions.ValidationError("座位数不能少于50！")

# 计算出session 中所选择的attendee的个数
	@api.depends("attendee_ids")
	def _get_attendees_count(self):
		for session in self:
			session.attendees_count = len(session.attendee_ids)
	@api.multi
	@api.depends("start_date","duration")
	def _get_end_date(self):
		for session in self:
			if not(session.start_date and session.duration):
				session.end_date = session.start_date
				continue
			start_date = fields.Datetime.from_string(session.start_date)
			duration = timedelta(days = session.duration-1)
			session.end_date = start_date + duration

	@api.onchange("start_date","end_date")
	def change_Duration(self):
		for session in self:
			if not (session.start_date and session.end_date):
				continue
			start_date = fields.Datetime.from_string(session.start_date)
			end_date = fields.Datetime.from_string(session.end_date)
			session.duration = (end_date - start_date).days + 1

	@api.depends("attendee_ids")
	def get_attendee_ids(self):
		for session in self:
			session.num_attendee = len(session.attendee_ids)
	@api.onchange("seats","attendee_ids")
	def verify_valid_seats(self):
		if self.seats < 0:
			return{
			"warning":{
					"title":"温馨提示",
					"message":"座位数不能为负数！",
				}
			}
		if self.seats < len(self.attendee_ids):
			return{
				"warning":{
					"title":"温馨提示",
					"message":"学生数不能大于座位数！",
				}
			}
	@api.constrains("seats","attendee_ids")
	def _seats_and_attendees_constrains(self):
		for session in self:
			if session.seats < len(session.attendee_ids):
				raise exceptions.ValidationError("选择的学生数不能大于座位数！")
			if session.seats < 0:
				raise exceptions.ValidationError("座位数不能为负数！")
			if session.seats < 50:
				raise exceptions.ValidationError("座位数不能少于50！")

	




	
	




