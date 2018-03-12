"""Interface AiiDA <-> parsevasp.poscar."""
import sys

import numpy as np
from aiida.common.log import aiidalogger
from parsevasp.poscar import Poscar, Site


class ParseVaspToAiidaPoscar(object):
    """A wrapper to embed parsevasp POSCAR into Aiida."""

    def __init__(self, file_path=None, string=None, astructure=None, logger=aiidalogger, comment=None):
        self._logger = logger
        # make sure only one is set
        params_given = [bool(param is not None) for param in [file_path, string, astructure]]
        if sum(params_given) > 1:
            self._logger.error("Please only supply one parameter " "when initializing ParseVaspToAiidaPoscar.")
            sys.exit(1)
        # if an Aiida structure object is passed, convert this
        if astructure is not None:
            dictionary = {}
            dictionary["comment"] = comment or ''
            dictionary["unitcell"] = np.array(astructure.cell)
            asites = astructure.sites
            sites = []
            for site in asites:
                specie = site.kind_name
                position = site.position
                sites.append(Site(specie, position))
            dictionary["sites"] = sites

        self._poscar = Poscar(logger=logger, file_path=file_path, poscar_string=string, poscar_dict=dictionary)

    def write(self, file_path):
        self._poscar.write(file_path=file_path)
