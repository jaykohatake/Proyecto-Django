import os
from django.contrib.gis.utils import LayerMapping
from .models import Point

centroidesPredio_mapping = {
    'code_predi' : 'Code_Predi',
    'geom' : 'POINT',

}

centroidesPredio_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'centroides_rut.shp'),
)

def run(verbose=True):
    lm = LayerMapping(
        Point, centroidesPredio_shp, centroidesPredio_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)