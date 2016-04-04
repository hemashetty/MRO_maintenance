
from openerp import models, fields, api


class Wizard(models.TransientModel):
    _name = 'mro_module.wizard'
    wiz_cont = fields.Char(string="Contact Name", index="True")

    wiz_title = fields.Char(string="Title", index="True")
    wiz_post = fields.Char(string="Job Position", index="True")
    wiz_emil = fields.Char(string="Email", index="True")
    wiz_phn = fields.Char(string="Phone", index="True")
    wiz_mob = fields.Char(string="Mobile", index="True")
    wiz_note = fields.Text(string="Notes", index="True")
    wiz_type = fields.Boolean(string="Contact", index="True")
    wiz_add = fields.Char(string="Address", index="True")


# address
class Addres(models.TransientModel):
    _name = 'mro_module.addres'
    add_addr = fields.Char(string="Address", index="True")
