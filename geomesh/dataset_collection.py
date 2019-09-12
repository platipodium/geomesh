from pathlib import Path
from geomesh.gdal_dataset import GdalDataset


class DatasetCollection:

    def __init__(self):
        self.__container = list()

    def __iter__(self):
        for gdal_dataset in self.__container:
            yield gdal_dataset

    def add_dataset(self, gdal_dataset):
        if isinstance(gdal_dataset, (str, Path)):
            gdal_dataset = GdalDataset(gdal_dataset)
        else:
            assert isinstance(gdal_dataset, GdalDataset)
        exist = False
        for _ in self.__container:
            if gdal_dataset.path == _.path:
                exist = True
                break
        if not exist:
            self.__container.append(gdal_dataset)
