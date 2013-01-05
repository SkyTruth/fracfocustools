# -*- coding: utf-8 -*-

from .context import FracFocusPDFParser
from .context import Logger

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""


    def parse_pdf (self, filename):
        logger = Logger ()
        f = open(filename, 'r')
        raw_pdf = f.read()
        parser = FracFocusPDFParser (raw_pdf, logger)
        
        print 'parsing pdf %s...' %filename
        report = parser.parse_pdf ()
        
        print logger.get_messages ()
        assert (not logger.has_error())
        
        return report, logger
    
    def test_Parser(self):
        
        report,logger = self.parse_pdf ('./tests/data/4200344349-8272012-242-CHESAPEAKE.pdf')

        assert (report.report_data['api'] == '4200344349')
        assert (report.report_data['total_water_volume'] == '975,492')
        assert (report.chemicals[0]['trade_name'] == 'Fresh Water')
        assert (report.chemicals[1]['cas_number'] == '007732-18-5')

# TODO: This should work, need to fix the multi-line problem
#        assert (report.chemicals[1]['supplier'] == 'FTS INTERNATIONAL')

        
     
    def test_IngredientWeight (self):        
        
        report,logger = self.parse_pdf ('./tests/data/0403045721-8152012-978-Aera Energy Llc.pdf')

        assert (report.report_data['fracture_date'] == '08/15/2012')
        assert (report.chemicals[0]['ingredient_weight'] == '284,177')
        assert (report.chemicals[1]['ingredient_weight'] == '0.600000')
    
    def test_missing_total_water_volume (self):
        report,logger = self.parse_pdf ('./tests/data/43013512780000-1172012-186-Bill Barrett Corp.pdf')

        assert (report.report_data['fracture_date'] == '11/07/2012')

        assert (logger.has_message('warning', 'Missing report field: total_water_volume'))


    
#    def test_ParseFail (self):
#        # This pdf causes an assertion in pdfminer.  Maybe a future update will fix it?
#        report = self.parse_pdf ('./tests/data/4216537646-10292012-617-Citation Oil and Gas Corp.pdf')
        
if __name__ == '__main__':
    unittest.main()