# -*- coding: utf-8 -*-

from openerp import models, fields, api


class MaintainanceRequest(models.Model):
    _name = 'mro_module.maintenance_request'
    _inherit = ['mail.thread']

    name = fields.Char(string="Reference")
   # req_date = fields.Date(string="Requested Date", ondelete='set null', index=True)
    req_date = fields.Datetime(
        string="Requested Date", default=fields.Datetime.now)
    exec_date = fields.Datetime(
        string="Execution Date", default=fields.Datetime.now)

    Cause = fields.Char(string="Cause", ondelete='set null', index="True")
    Breakdown = fields.Boolean('Breakdown')
    product_id = fields.Many2one('product.template', string="Product")
    description = fields.Text("")
    state = fields.Selection([
        ('draft', 'DRAFT'),
        ('claim', 'CLAIM'),
        ('execution', 'EXECUTION'),
        ('done', 'DONE'),
        ('rejected', 'REJECTED'),
        ('cancel', 'CANCELED')
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_claim(self):
        self.state = 'claim'
        order_values = {
            'name': self.name,
            'maintenance_type': 'bd' if self.Breakdown else 'ct',
            'description': self.description,
            'execution_date': self.exec_date,
            'request_id': self.id
        }
        self.env['mro_module.maintenance_order'].create(order_values)

    @api.multi
    def action_reject(self):
        self.state = 'rejected'

    @api.multi
    def action_execution(self):
        self.state = 'execution'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'


class MaintainanceOrder(models.Model):
    _name = 'mro_module.maintenance_order'
    _inherit = ['mail.thread']

    MAINTENANCE_TYPE_SELECTION = [
       ('bd', 'Breakdown'),
       ('ct', 'Corrective')
    ]

    name = fields.Char(string="Reference")
    request_id = fields.Many2one('mro_module.maintenance_request', 'Request')
    product_id = fields.Many2one(related='request_id.product_id')
    maintenance_type = fields.Selection(
        selection=MAINTENANCE_TYPE_SELECTION, string='Maintenance Type',
    readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Text()
    part_ids = fields.Many2many('product.template', domain="[('categ_id.name', '=', 'Parts')]")
    planned_date = fields.Date(default=fields.Date.today)
    scheduled_date = fields.Date(default=fields.Date.today)
    execution_date = fields.Date(default=fields.Date.today)
    source_document = fields.Char(string="source_document")
    state = fields.Selection([
        ('draft', 'DRAFT'),
        ('released', 'WAITING PARTS'),
        ('inprocess', 'IN PROCESS'),
        ('done', 'DONE'),
        ('cancel', 'CANCELED')
    ], default='draft')

    @api.multi
    def action_draft(self):
        self.state = 'draft'

    @api.multi
    def action_released(self):
        self.state = 'released'

    @api.multi
    def action_inprocess(self):
        self.state = 'inprocess'

    @api.multi
    def action_done(self):
        self.state = 'done'

    @api.multi
    def action_cancel(self):
        self.state = 'cancel'




# Detail of product

class Maint_produ(models.Model):
    _name = 'mro_module.maint_produ'

    #prod_loc = fields.Char(string="Product location")
    tag = fields.Many2many('ir.attachment')

    prod_loc = fields.Many2one(
        'mro_module.maint_loc', ondelete='cascade', string="Product location", required=True)
    critic = fields.Char(string="Criticality")
#    assign = fields.Char(string="Assigned to")
    assign = fields.Many2one(
        'res.users', string="Assigned to", ondelete='set null', index=True)
    active = fields.Boolean('Active')
    prod_no = fields.Integer(string="Product Number")
    prod_mod = fields.Char(string="Model")
    prod_ser = fields.Integer(string="Serial no.")
    #prod_manu = fields.Char(string="Manufacturer", required=True)
#    prod_manu = fields.Many2one('mro_module.maint_manuf', ondelete='cascade', string="Manufacturer", required=True)
    prod_manu = fields.Many2one(
        'res.partner', ondelete='cascade', string="Manufacturer")
    prod_dt_st = fields.Date(string="Start Date")
    prod_dt_wrnty = fields.Date(string="Warranty Start")
    prod_vend = fields.Many2one(
        'res.partner', string="Vendor", ondelete='cascade')
    prod_pur_dt = fields.Date(string="Purchase Date")
    prod_war_end = fields.Date(string="Warranty End")
# location of product


class Maint_loc(models.Model):
    _name = 'mro_module.maint_loc'
    loc_type = fields.Char(string="Location Type")
    loc_owner = fields.Char(string="Owner")
    loc_scrap = fields.Boolean('Is a scrap location?')
    loc_return = fields.Boolean('Is a return location?')
    loc_active = fields.Boolean('Active')
    #loc_localize = fields.Char(string="Localization", required=True)
    loc_corridor = fields.Char(string="Corridor(X)")
    loc_shelves = fields.Char(string="Shelves(Y)")
    loc_height = fields.Char(string="Height(Z)")
    loc_barcode = fields.Char(string="Barcode")


# manufacturer detail
class Maint_manuf(models.Model):
    _name = 'mro_module.maint_manuf'
    manuf_add = fields.Char(string="Address")
    manuf_website = fields.Char(string="Website", index=True)
    manuf_job_post = fields.Char(string="Job Position", index=True)
    manuf_phn = fields.Char(string="Phone", index=True)
    manuf_mob = fields.Char(string="Mobile", index=True)
    manuf_fax = fields.Char(string="Fax", index=True)
    manuf_eml = fields.Char(string="Email", index=True)
    manuf_title = fields.Char(string="Titile", index="True")
    manuf_lang = fields.Char(string="Language")
    manuf_tags = fields.Char(string="Tags", index="True")
    manuf_cont = fields.Many2one(
        'mro_module.maint_vend', ondelete='cascade', string="Contact")
    # function of contact field
    manuf_int = fields.Char(string="")
    manuf_desc = fields.Text(defaults="Internal notes", index="True")

    manuf_cust = fields.Boolean(string="Is a Customer", index="True")
    manuf_sale = fields.Many2one(
        'res.users', string="Salesperson", index="True")
    manuf_vend = fields.Boolean(string="Is a vendor", index="True")
    manuf_intref = fields.Char(string="Internal Reference", index="True")
    manuf_bnk_act = fields.Many2one('mro_module.maint_vend', readonly="True")

# vendor detail


class Maint_vend(models.Model):
    _name = 'mro_module.maint_vend'
    vend_add = fields.Char(string="Address")
    vend_website = fields.Char(string="Website", index=True)
    vend_job_post = fields.Char(string="Job Position", index=True)
    vend_phn = fields.Char(string="Phone", index=True)
    vend_mob = fields.Char(string="Mobile", index=True)
    vend_fax = fields.Char(string="Fax", index=True)
    vend_eml = fields.Char(string="Email", index=True)
    vend_title = fields.Char(string="Titile", index="True")
    vend_lang = fields.Char(string="Language")
    vend_tags = fields.Char(string="Tags", index="True")

# Contact detail


class Maint_cont(models.Model):
    _name = 'mro_module.maint_cont'
    cont_nm = fields.Char(string="Contact Name", index="True")
    cont_title = fields.Char(string="Title", index="True")
    cont_job_post = fields.Char(string="Job Position", index="True")
    cont_eml = fields.Char(string="Email", index=True)
    cont_phn = fields.Char(string="Phone", index=True)
    cont_mob = fields.Char(string="Mobile", index=True)
    cont_note = fields.Char(string="Notes", index=True)
