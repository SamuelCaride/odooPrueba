
from fields.extras import ValidationError
import fields
import api
import models

# autorizado = fields.Boolean(string="¿Autorizado?", default=True)

class informacion:

    alto_en_cms = fields.Integer(string="Alto en centímetros")
    longo_en_cms = fields.Integer(string="Longo en centímetros")
    ancho_en_cms = fields.Integer(string="Ancho en centímetros")
    volume = fields.Float(compute="_volume", store=True)

    @api.depends('alto_en_cms', 'longo_en_cms', 'ancho_en_cms')
    def _volume(self):
        for rexistro in self:
            rexistro.volume = float(rexistro.alto_en_cms) * float(rexistro.longo_en_cms) * float(rexistro.ancho_en_cms)


    literal = fields.Char(store=False)

    @api.onchange('alto_en_cms')
    def _avisoAlto(self):
        for rexistro in self:
            if rexistro.alto_en_cms > 7:
                rexistro.literal = 'O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_en_cms
            else:
                rexistro.literal = ""

    peso = fields.Float(digits=(6, 2), string="Peso en Kg.s", default=2.7)

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)

    _sql_constraints = [('nomeUnico', 'unique(name)', 'Non se pode repetir o nome')]

    _order = "descripcion desc"
