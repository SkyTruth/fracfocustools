#

from pdfminer.layout import LTContainer, LTComponent, LTRect, LTLine, LAParams, LTTextLine
from pdfminer.utils import Plane


class Logger (object):

    def __init__(self):
        self.messages = []

    def log(self, severity, message):
        self.messages.append({'severity':severity, 'message': message})

    def warning (self, message):
        self.log('warning', message)

    def error (self, message):
        self.log('error', message)

    def has_error (self):
        for m in self.messages:
            if m['severity'] == 'error': return True
        return False

    def has_warning (self):
        for m in self.messages:
            if m['severity'] == 'warning': return True
        return False

    def has_message (self, severity, message):
        for m in self.messages:
            if m['severity'] == severity and m['message'] == message : return True
        return False

    def get_messages (self):
        return '\n'.join(['%(severity)s: %(message)s' % (m) for m in self.messages])


class CellText (LTComponent):
    text = ''

    def __init__(self, bbox, text):
        LTComponent.__init__ (self, bbox)
        self.text = text

class Cell (LTComponent):
    text_lines = None

    def __init__(self, bbox):
        LTComponent.__init__ (self, bbox)
        self.text_lines = []

    def get_text (self):
        return ' '.join ([t.text for t in self.text_lines])

class Sheet1 (object):
    cells = None
    text_layout = None
    column_edges = None
    row_edges = None


    def __init__(self):
        self.cells = Plane()
        self.text_layout = Plane()
        self.row_edges = {}
        self.column_edges = {}

    def add_cell (self, cell):
        self.cells.add(cell)


    def add_text (self, cell_text):
        self.text_layout.add(cell_text)
#        if cell_text.text[:3] == 'Oil': print cell_text.text, cell_text.bbox

    def add_column_edge (self, x_value):
        x = round(x_value,2)
        self.column_edges[x] = 1+ self.column_edges.get(x,0)

    def add_row_edge (self, y_value):
        y = round(y_value,2)
        self.row_edges[y] = 1+ self.row_edges.get(y,0)

    def add_line (self, bbox):
        if bbox[0]==bbox[2]:
            # vertical line
            self.add_column_edge(bbox[0])
        elif bbox[1]==bbox[3]:
            #horizontal line
            self.add_row_edge(bbox[1])
        else:
            print ('WARNING: non-orthogonal line found: %s'%bbox)

    def add_rect (self, bbox):
        self.add_column_edge(bbox[0])
        self.add_column_edge(bbox[2])
        self.add_row_edge(bbox[1])
        self.add_row_edge(bbox[3])

    def add_ltcontainer (self, obj, page_y_offset):
        #NB: row indexes (y axis) are negative!

        bbox = (
            round(obj.x0,2),
            round(-(obj.y1+page_y_offset),2),
            round(obj.x1,2),
            round(-(obj.y0+page_y_offset),2)
            )

        if isinstance (obj, LTTextLine):
            self.add_text (CellText(bbox, obj.get_text()))
        elif isinstance (obj, LTLine):
            self.add_line(bbox)
        elif isinstance (obj, LTRect):
            self.add_rect(bbox)
        elif isinstance (obj, LTContainer):
            for child in obj:
                self.add_ltcontainer (child, page_y_offset)
        else:
            pass

    def extract_rows (self):
#        for obj in self.text_layout.find((690, -1200, 800, -1000)):
#            print obj.bbox,obj.text

        row_bounds = sorted(self.row_edges)
        col_bounds = sorted(self.column_edges)

#        pprint.pprint(col_bounds)

        rows = []

        r0 = row_bounds[0] - 1 if row_bounds else 0

        #NB: row indexes (y axis) are negative!
        for r1 in row_bounds:
            if r1 - r0 < 1: continue

#            print r1-r0,r0,r1

            row=[]
            c0 = 0
            for c1 in col_bounds:
                if c1 - c0 < 1: continue

#                print c0,r0,c1,r1
                # get all text lines that intersect the bounds of this cell
                lines = [l for l in self.text_layout.find((c0,r0,c1,r1))]
                #sort from top to bottom
                lines = sorted(lines, key=lambda line: line.y0)

#                text = ' '.join([t.text.strip() for t in lines if t.x0 >= c0 and t.x0 <= c1])
#                if text[:10] == 'Production': print text,c0,r0,c1,r1
#                if text[:3] == 'Oil': print text,c0,r0,c1,r1

                # remove anything where the left edge is not inside the cell and concatenate the rest
                row.append(' '.join([t.text.strip() for t in lines if t.x0 >= c0 and t.x0 <= c1]))
                c0 = c1
            rows.append(row)
            r0 = r1
        return rows
