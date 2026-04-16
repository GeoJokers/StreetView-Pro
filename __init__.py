# -*- coding: utf-8 -*-

def classFactory(iface):
    from .streetviewpro import StreetViewPro
    return StreetViewPro(iface)