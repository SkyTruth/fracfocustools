# -*- coding: utf-8 -*-

from StringIO import StringIO
import sys, traceback
import re


from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LTContainer, LTComponent, LTRect, LTLine, LAParams, LTTextLine
from pdfminer.utils import Plane
from pdfminer.converter import PDFPageAggregator

from helpers import Sheet

class Report (object):
    field_defs = None
    report_data = None
    col_indexes = None
    messages = None
    chemicals = None
    
    def __init__ (self, logger):
        self.field_defs = [
            {'label':'fracture_date', 'regex': 'fracturedate:?$', 'type': 'report'},
            {'label':'fracture_date', 'regex': 'lastfracturedate:?$', 'type': 'report'},
            {'label':'state', 'regex': 'state:?$', 'type': 'report'},
            {'label':'county', 'regex': 'county:?$', 'type': 'report'},
            {'label':'county', 'regex': 'county/parish:?$', 'type': 'report'},
            {'label':'api', 'regex': 'apinumber:?$', 'type': 'report'},
            {'label':'operator', 'regex': 'operatorname:?$', 'type': 'report'},
            {'label':'well_name', 'regex': 'wellnameandnumber:?$', 'type': 'report'},
            {'label':'longitude', 'regex': 'longitude:?$', 'type': 'report'},
            {'label':'latitude', 'regex': 'latitude:?$', 'type': 'report'},
            {'label':'datum', 'regex': 'long/latprojection:?$', 'type': 'report'},
            {'label':'production_type', 'regex': 'productiontype:?$', 'type': 'report'},
            {'label':'true_vertical_depth', 'regex': 'trueverticaldepth.*$', 'type': 'report'},
            {'label':'total_water_volume', 'regex': 'totalwatervolume.*$', 'type': 'report', 'optional': True},
            {'label':'trade_name', 'regex': 'tradename$', 'type': 'column'},
            {'label':'supplier', 'regex': 'supplier$', 'type': 'column'},
            {'label':'purpose', 'regex': 'purpose$', 'type': 'column'},
            {'label':'ingredients', 'regex': 'ingredients$', 'type': 'column'},
            {'label':'cas_number', 'regex': 'chemicalabstractservicenumber', 'type': 'column'},
            {'label':'additive_concentration', 'regex': 'maximumingredientconcentrationinadditive', 'type': 'column'},
            {'label':'hf_fluid_concentration', 'regex': 'maximumingredientconcentrationinhffluid', 'type': 'column', 'optional':True},
            {'label':'ingredient_weight', 'regex': 'maximumingredientweight', 'type': 'column', 'optional': True},
            {'label':'comments', 'regex': 'comments$', 'type': 'column'},
            {'label':'footer', 'regex': '\*totalwatervolumesourcesmayinclude', 'type': 'footer'},
            {'label':'footer', 'regex': '\*totalchemicalmassisthetotalamountof', 'type': 'footer'},
        ]
        self.report_data = {}
        self.col_indexes = {}
        self.messages = []
        self.chemicals = []
        self.logger = logger
    
    def warning (self, msg):
        self.logger.warning(msg)

    def error (self, msg):
        self.logger.error(msg)
        
    def match_field_def (self, text, field_def):
        t = re.sub('[\s]','',text)
        return re.match(field_def['regex'], t, re.IGNORECASE)
    
    def find_field_def (self, text):
        t = re.sub('[\s]','',text)
        for d in self.field_defs:
            if re.match(d['regex'], t, re.IGNORECASE):
                return d
        return None
    
    def row_contains_label (self, row):
        for col in row:
            field_def = self.find_field_def (col)
            if field_def: return field_def
        return None

    def extract_report_field (self, field_def, row):
        text= []
        
        for col in row:
#            print field_def['label'],col
            # skip data that matches the field label
            if col and not self.match_field_def(col,field_def):
                #take only the first non-blank column that does not match the field label
                if col:
                    text.append (col)
                    break
            
        self.report_data [field_def['label']] = ' '.join(text)
        
    def extract_column_headings (self, row):
        for i,text in enumerate(row):
            if text:
                field_def = self.find_field_def(text)
                if field_def and field_def['type'] == 'column':
                    self.col_indexes[field_def['label']] = i
                else:
                    self.warning('Unknown column heading: %s'%text)
        
        # check to see that we got all the coluumn headings
        expected_count = 0
        for d in self.field_defs:
            if d['type'] == 'column' and not d.get('optional'): 
                expected_count += 1
                if d['label'] not in self.col_indexes:
                    self.error('Missing column header: %s' %d['label'])
            
                
        if len(self.col_indexes) < expected_count:
            self.error('Wrong columnn heading count - expected: %s, found: %s'%(expected_count, len(self.col_indexes)))
            
    def extract_chemical_record (self, row, chem_row_number):
        record = {'row': chem_row_number}
        for label,i in self.col_indexes.items():
            record[label] = row[i]
            
        self.chemicals.append(record)
    
    def extract_data (self, sheet):
        rows = sheet.extract_rows()
        
        found_col_header = False
        chem_row_number = 1
        
        for row in rows:
            field_def = self.row_contains_label (row)

            if found_col_header:
                # if we have already seen the column header row, extract a chemical record and add to the list of chemicals

                if field_def and field_def['type'] == 'footer':
                    # found the footer - no more data after this
                    break
                if ''.join(row):
                    # don't extract empty rows
                    self.extract_chemical_record (row, chem_row_number)
                chem_row_number += 1
            elif field_def:
                # see if this row contains a defined label
                # if this is a report row, extract and add to the report 
                if field_def['type'] == 'report':
                    self.extract_report_field (field_def, row)
                elif field_def['type'] == 'column':
                    # if this is the column header row, extract and set column indexes
                    self.extract_column_headings(row)    
                    found_col_header = True  
            else:
#                print row 
                pass
                                    
        for d in self.field_defs:
            if d['type'] == 'report' and d['label'] not in self.report_data:
                if d.get('optional'):
                    self.warning('Missing report field: %s' %d['label'])
                else:
                    self.error('Missing report field: %s' %d['label'])


class FracFocusPDFParser (object):

    def __init__ (self, raw_pdf, logger):
        self.raw_pdf = raw_pdf
        self.logger = logger
        self.report = None
                    
    def parse_pdf (self):
        self.report = Report (self.logger)
        fp = StringIO(self.raw_pdf)
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        try:
            doc.set_parser(parser)
            doc.initialize('')
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
                            
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            sheet = Sheet()
            page_y_offset = 0
    
            pages = []
            for page in doc.get_pages():
                pages.append(page)
            pages.reverse()
                        
            for i,page in enumerate(pages):
                interpreter.process_page(page)
                layout = device.get_result()
                sheet.add_ltcontainer (layout, page_y_offset)
                page_y_offset += layout.y1
                
            self.report.extract_data (sheet)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            trace = traceback.format_exception (exc_type, exc_value, exc_traceback)        
            self.logger.error('%s'%''.join(trace))
        
        if self.logger.has_error():
            return None
        else:
            return self.report