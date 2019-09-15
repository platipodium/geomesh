import numpy as np
import matplotlib.pyplot as plt
from osgeo import ogr
from jigsawpy import jigsaw_msh_t
import geomesh
from geomesh.gdal_tools import GdalTools


class PlanarStraightLineGraph(GdalTools):

    def __init__(self, DatasetCollection, zmin, zmax, SpatialReference=3395):
        super(PlanarStraightLineGraph, self).__init__()
        self._zmin = zmin
        self._zmax = zmax
        self._SpatialReference = SpatialReference
        self._DatasetCollection = DatasetCollection

    def __iter__(self):
        for gdal_dataset in self._DatasetCollection:
            yield gdal_dataset

    def make_plot(self, show=False):
        for _Polygon in self.MultiPolygon:
            for _LinearRing in _Polygon:
                _LinearRing = _LinearRing.Clone()
                array = np.asarray(_LinearRing.GetPoints())
                plt.plot(array[:, 0], array[:, 1])
        plt.gca().axis('scaled')
        if show:
            plt.show()
        return plt.gca()

    @property
    def SpatialReference(self):
        return self.__SpatialReference

    @property
    def Polygon(self):
        try:
            return self.__Polygon
        except AttributeError:
            pass
        _MultiPolygon = self.MultiPolygon
        areas = [_Polygon.GetArea() for _Polygon in _MultiPolygon]
        idx = int(np.where(areas == np.max(areas))[0][0])
        _Polygon = _MultiPolygon.GetGeometryRef(idx)
        self.__Polygon = _Polygon.Clone()
        return self.__Polygon

    @property
    def MultiPolygon(self):
        try:
            return self.__MultiPolygon
        except AttributeError:
            pass
        _MultiPolygon = ogr.Geometry(ogr.wkbMultiPolygon)
        _MultiPolygon.AssignSpatialReference(self.SpatialReference)
        for __MultiPolygon in list(self.MultiPolygons):
            for _Polygon in __MultiPolygon:
                _MultiPolygon.AddGeometry(_Polygon)
        _MultiPolygon = _MultiPolygon.Buffer(0)
        self.__MultiPolygon = _MultiPolygon
        return self.__MultiPolygon

    @property
    def MultiPolygons(self):
        _MultiPolygons = list()
        for gdal_dataset in self._DatasetCollection:
            gdal_dataset.zmin = self.zmin
            gdal_dataset.zmax = self.zmax
            _MultiPolygon = gdal_dataset.MultiPolygon
            _MultiPolygon.TransformTo(self.SpatialReference)
            _MultiPolygons.append(gdal_dataset.MultiPolygon)
        return _MultiPolygons

    @property
    def zmin(self):
        return self.__zmin

    @property
    def zmax(self):
        return self.__zmax

    @property
    def outer_vertices(self):
        _Polygon = self.Polygon
        _LinearRing_0 = _Polygon.GetGeometryRef(0)
        return np.asarray(_LinearRing_0.GetPoints())

    @property
    def inner_vertices(self):
        _Polygon = self.Polygon
        for i in enumerate(1, _Polygon.GetGeometryCount()):
            _LinearRing_i = _Polygon.GetGeometryRef(i)
            yield np.asarray(_LinearRing_i.GetPoints())

    @property
    def values(self):
        print(vert2)
        BREAKME

    @property
    def ocean_boundary(self):
        idx = np.where(self.values < 0)[0]
        return self.values[idx]

    @property
    def land_boundary(self):
        raise NotImplementedError

    @property
    def inflow_boundary(self):
        raise NotImplementedError

    @property
    def outflow_boundary(self):
        raise NotImplementedError

    @property
    def ocean_boundaries(self):
        for ds in self:
            bbox = ds.get_bbox(Path=True)
            if bbox.contains_point(self.outer_vertices[0, :]):
                # do something
                continue

            # if self.outer_vertices[-1]
        self.outer_vertices
        print(self.outer_vertices_values)
        BREAKEM
        # values = self._PlanarStraightLineGraph.values
        # ocean_boundary = np.where()
        # exit()

    @property
    def land_boundaries(self):
        raise NotImplementedError

    @property
    def inflow_boundaries(self):
        raise NotImplementedError

    @property
    def outflow_boundaries(self):
        raise NotImplementedError

    @property
    def mshID(self):
        return self._mshID

    @property
    def ndim(self):
        return self._ndim

    @property
    def vert2(self):
        try:
            return self.__vert2
        except AttributeError:
            vert2 = list()
            for _Polygon in self.MultiPolygon:
                for _LinearRing in _Polygon:
                    _vert2 = list()
                    for x, y in np.asarray(_LinearRing.GetPoints())[:-1, :2]:
                        _vert2.append(((x, y), 0))  # always 0?
                    vert2 = [*vert2, *_vert2]
            self.__vert2 = np.asarray(vert2, dtype=jigsaw_msh_t.VERT2_t)
            return self.__vert2

    @property
    def edge2(self):
        try:
            return self.__edge2
        except AttributeError:
            edge2 = list()
            for _Polygon in self.MultiPolygon:
                for _LinearRing in _Polygon:
                    _edge2 = list()
                    for i in range(_LinearRing.GetPointCount()-2):
                        _edge2.append((i, i+1))
                    _edge2.append((_edge2[-1][1], _edge2[0][0]))
                    _edge2 = np.asarray(_edge2) + len(edge2)
                    edge2 = [*edge2, *_edge2.tolist()]
            edge2 = [((x, y), 0) for x, y in edge2]
            self.__edge2 = np.asarray(edge2, dtype=jigsaw_msh_t.EDGE2_t)
            return self.__edge2

    @property
    def geom(self):
        geom = jigsaw_msh_t()
        geom.vert2 = self.vert2
        geom.edge2 = self.edge2
        geom.ndim = self.ndim
        geom.mshID = self.mshID
        return geom

    @property
    def _MultiPolygon(self):
        return self.__MultiPolygon

    @property
    def _zmin(self):
        return self.__zmin

    @property
    def _zmax(self):
        return self.__zmax

    @property
    def _ndim(self):
        return 2

    @property
    def _mshID(self):
        return 'euclidean-mesh'

    @property
    def _SpatialReference(self):
        return self.__SpatialReference

    @property
    def _DatasetCollection(self):
        for gdal_dataset in self.__DatasetCollection:
            gdal_dataset.zmin = self.zmin
            gdal_dataset.zmax = self.zmax
        return self.__DatasetCollection

    @SpatialReference.setter
    def SpatialReference(self, SpatialReference):
        curSRS = self.__SpatialReference
        dstSRS = self.sanitize_SpatialReference(SpatialReference)
        if not curSRS.IsSame(dstSRS):
            self.MultiPolygon.TransformTo(SpatialReference)
            if (curSRS.IsProjected() and dstSRS.IsGeographic()) or \
                    (curSRS.IsGeographic() and dstSRS.IsProjected()):
                self.MultiPolygon.SwapXY()
            self.__SpatialReference = dstSRS

    @_SpatialReference.setter
    def _SpatialReference(self, SpatialReference):
        dstSRS = self.sanitize_SpatialReference(SpatialReference)
        self.__SpatialReference = dstSRS

    @_DatasetCollection.setter
    def _DatasetCollection(self, DatasetCollection):
        assert isinstance(DatasetCollection,  geomesh.DatasetCollection)
        self.__DatasetCollection = DatasetCollection

    @_zmin.setter
    def _zmin(self, zmin):
        del(self._MultiPolygon)
        self.__zmin = float(zmin)

    @_zmax.setter
    def _zmax(self, zmax):
        del(self._MultiPolygon)
        self.__zmax = float(zmax)

    @_MultiPolygon.deleter
    def _MultiPolygon(self):
        try:
            del(self.__MultiPolygon)
        except AttributeError:
            pass

# from netCDF4 import Dataset
# pyenv_prefix = "/".join(sys.executable.split('/')[:-2])
# if os.getenv('SRTM15_PATH') is not None:
#     nc = pathlib.Path(os.getenv('SRTM15_PATH'))
# else:
#     nc = pathlib.Path(pyenv_prefix + '/lib/SRTM15+V2.nc')

# points = np.asarray(_LineString.GetPoints())
# cx = np.sum(points[:-1, 0]) / 4
# cy = np.sum(points[:-1, 1]) / 4
# dd1 = np.sqrt(np.abs(cx-points[0][0])) \
#     + np.sqrt(np.abs(cy-points[0][1]))
# dd2 = np.sqrt(np.abs(cx-points[1][0])) \
#     + np.sqrt(np.abs(cy-points[1][1]))
# dd3 = np.sqrt(np.abs(cx-points[2][0])) \
#     + np.sqrt(np.abs(cy-points[2][1]))
# dd4 = np.sqrt(np.abs(cx-points[3][0])) \
#     + np.sqrt(np.abs(cy-points[3][1]))
# if dd1 - dd2 < 1e-3 and \
#         dd1 - dd3 < 1e-3 and dd1 - dd4 < 1e-3:
# _Polygon.RemoveGeometry(i)