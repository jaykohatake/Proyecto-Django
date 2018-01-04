# -*- coding: utf-8 -*-
import os
from django.contrib.gis.utils import LayerMapping
from .models import Barrio, Point
from django.contrib.gis import geos

barrio_mapping = {
    'codigo_bar' : 'CODIGO_BAR',
    'area' : 'AREA',
    'perimetro' : 'PERIMETRO',
    'nmg' : 'NMG',
    'geom' : 'MULTIPOLYGON',
}

barrio_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'Barrio.shp'))
point_csv = os.path.abspath(os.path.join('SIRICWEB','data', 'coordenadas.csv'))

def run(verbose=True):
    lm = LayerMapping(
        Barrio, barrio_shp, barrio_mapping,
        transform=False, encoding='utf-8',
    )
    lm.save(strict=True, verbose=verbose)

def point_load():
    with open(point_csv) as point_file:
        for line in point_file:
            code_predi, lon, lat = line.split(';')
            point = "POINT(%s %s)" % (lat.strip(), lon.strip())
            Point.objects.create(code_predi=code_predi, geom=geos.fromstr(point))