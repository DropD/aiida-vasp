"""AiiDA Parser for aiida_vasp.Vasp2W90Calculation"""
from aiida.orm import DataFactory

from .vasp import VaspParser
from ..utils.io.win import WinParser


class Vasp2w90Parser(VaspParser):
    """Parse a finished aiida_vasp.Vasp2W90Calculation"""

    def parse_with_retrieved(self, retrieved):
        super(Vasp2w90Parser, self).parse_with_retrieved(retrieved)

        has_win, win_node = self.get_win_node()
        has_full_dat, dat_node = self.get_wdat_node()
        self.set_win(win_node)
        self.set_wdat(dat_node)

        return self.result(success=has_win and has_full_dat)

    def get_win_node(self):
        """Create the wannier90 .win file output node"""
        win = self.get_file('wannier90.win')
        if not win:
            return False, None
        win_parser = WinParser(win)
        winnode = DataFactory('parameter')(dict=win_parser.result)
        return True, winnode

    def get_wdat_node(self):
        """Create the wannier90 data output node comprised of the .mmn, .amn, .eig files"""
        wdatnode = DataFactory('vasp.archive')()
        success = True
        for ext in ['mmn', 'amn', 'eig']:
            wfile = self.get_file('wannier90.' + ext)
            if wfile:
                wdatnode.add_file(wfile)
            else:
                success = False
        return success, wdatnode

    def set_win(self, node):
        if node:
            self.add_node('wannier_parameters', node)

    def set_wdat(self, node):
        if node:
            self.add_node('wannier_data', node)
