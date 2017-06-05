
from openerp import fields, api, models
from openerp.addons.base_geoengine import geo_model
from openerp.addons.base_geoengine import fields as geo_fields
from openerp.exceptions import ValidationError
import utm
try:
    from shapely.geometry import Point
    from shapely.wkb import loads as wkbloads
    import geojson
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning('Shapely or geojson are not available in the sys path')


class Dustbin(geo_model.GeoModel):
    _name = "dustbin.dustbin"
    the_point = geo_fields.GeoPoint('Coordinate')
    long = fields.Float("Longitude", digits=(16, 6))
    lat = fields.Float("Latitude", digits=(16, 6))
    name = fields.Char('Dustbin Name', size=64, required=True)
    code = fields.Many2one('dustbin.code', 'Dustbin Code', required=True)
    type = fields.Selection([('view', 'View'),
                             ('normal', 'Normal')],
                            'Type',
                            default='normal',
                            readonly=True)
    state = fields.Selection([('empty', 'Empty'),
                              ('full', 'Full')], 'Status',
                             index=True,
                             required=True)
    thepoi = fields.Char(compute='_compute_char')

    @api.depends('long', 'lat')
    def _compute_geo(self):
        latitude = self.lat and float(self.lat)
        longitude = self.long and float(self.long)

        self.the_point = geo_fields.GeoPoint.from_latlon(self.env.cr, latitude, longitude)


    @api.depends('the_point')
    def _compute_char(self):
        self.thepoi = str(self.the_point)
        '''
        if self.lat and self.long:
            self.lat = self.lat and float(self.lat)
            self.lon = self.long and float(self.long)
            #(field.GeoPoint.from_latlon(self.env.cr, self.lat, self.long)) 
            '''

    _sql_constraints = [
        ('code_unique',
         'UNIQUE(code)',
         "The Dustbin Code must be unique"),
        ('name_unique',
         'UNIQUE(name)',
         "The Dustbin Name must be unique"),
    ]


class DustbinCode(models.Model):
    _name = 'dustbin.code'
    name = fields.Char(String="Code")
    _sql_constraints = [
        ('code_unique',
         'UNIQUE(name)',
         "The Code must be unique")
    ]

