import os
from django.contrib.gis.utils import LayerMapping
from .models import CoordenadasPredio

coordenadaspredio_mapping = {
    'obs' : 'Obs',
    'id_lote' : 'ID_LOTE',
    'zona' : 'Zona',
    'met_riego' : 'MET_RIEGO',
    'prop' : 'PROP',
    'fecha_siem' : 'Fecha_siem',
    'code_predi' : 'Code_Predi',
    'month' : 'Month',
    'year' : 'Year',
    'area_ha' : 'Area_ha',
    'geom' : 'MULTIPOLYGON',
}

coordenadaspredio_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Predios_codes.shp'),
)

def run(verbose=True):
    lm = LayerMapping(
        CoordenadasPredio, coordenadaspredio_shp, coordenadaspredio_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)