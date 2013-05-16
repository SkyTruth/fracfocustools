#
import re

from pdfminer.layout import LTContainer, LTRect, LTLine, LTTextLine

ROUND_LEVEL = 1
HDR_ROW_THRESH = 7


class Element(object):
    def __init__(self, bbox):
        self.bbox = (round(bbox[0], ROUND_LEVEL),
                     round(bbox[1], ROUND_LEVEL),
                     round(bbox[2], ROUND_LEVEL),
                     round(bbox[3], ROUND_LEVEL)
                    )
        self.cent = (round((bbox[0] + bbox[2]) / 2, ROUND_LEVEL),
                     round((bbox[1] + bbox[3]) / 2, ROUND_LEVEL))
        self.area = round(abs((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])),
                          ROUND_LEVEL)
        self.row = None
        self.col = None
        self.orphan = False

class Rect(Element):
    _rectlist = []
    _is_assigned = False
    num_rows = None
    hdr_row = 0

    def __init__(self, bbox):
        Element.__init__(self, bbox)
        Rect._rectlist.append(self)
        Rect._is_assigned = False

    def __unicode__(self):
        return (u"Rect[%s, %s]: @%s (%s)"
                % (self.row, self.col, self.area, self.bbox))

    @classmethod
    def clear(cls):
        cls._rectlist = []
        cls._is_assigned = False

    @classmethod
    def _eliminate_dups(cls):
        cls._rectlist.sort(key=lambda r:r.cent[1])
        cls._rectlist.sort(key=lambda r:r.cent[0])
        dups = []
        for i_, rect in enumerate(cls._rectlist[:-1]):
            if rect.bbox == cls._rectlist[i_+1].bbox:
                dups.append(i_)
        #print ("Rect eliminating %s dups from list of %s."
        #       %(len(dups), len(cls._rectlist)))
        dups.reverse()
        for i_ in dups:
            del cls._rectlist[i_]

    @classmethod
    def find_rect(cls, cent):
        rtn = None
        for rect in cls._rectlist:
            if (    rect.bbox[0] <= cent[0] <= rect.bbox[2] and
                    rect.bbox[1] <= cent[1] <= rect.bbox[3] ):
                if rtn is None:
                    rtn = rect
                else:
                    #print ("OVERLAP: centroid %s in multiple rects: %s, %s"
                    #        % (cent, rtn, rect))
                    # select the rect with the smaller area
                    if rtn.area > rect.area:
                        rtn = rect
        return rtn

    @classmethod
    def _assign_rows(cls):
        # sort by y to find rows
        cls._rectlist.sort(key=lambda r:r.bbox[1])
        span = cls._rectlist[0].bbox[3] - cls._rectlist[-1].bbox[1]
        thresh = abs(span / len(cls._rectlist))
        row = 0
        row_count = 0
        last_y = cls._rectlist[0].bbox[1]
        for rect in cls._rectlist:
            if (rect.bbox[1] - last_y) > thresh:
                if not cls.hdr_row and row_count > HDR_ROW_THRESH:
                    cls.hdr_row = row
                row += 1
                row_count = 0
            rect.row = row
            row_count += 1
            last_y = rect.bbox[1]
        Rect.num_rows = row
        #print ("Rect._assign_rows: %s rows, thresh %s " % (row, thresh))

    @classmethod
    def _assign_cols(cls):
        # sort by x, then by row to find cols
        # this relies on python's stable sort
        cls._rectlist.sort(key=lambda r:r.cent[0])
        cls._rectlist.sort(key=lambda r:r.row)

        col = 0
        last_row = cls._rectlist[0].row
        for rect in cls._rectlist:
            if rect.row != last_row:
                last_row = rect.row
                col = 0
            rect.col = col
            #print "Assigned column: %s" % rect
            col += 1

    @classmethod
    def _check_cols(cls):
        #print "_check_cols: Rect.hdr_row:", cls.hdr_row
        if not cls.hdr_row:
            return
        for rect1 in cls._rectlist:
            if rect1.row != cls.hdr_row: continue
            for rect2 in cls._rectlist:
                if rect2.row <= cls.hdr_row: continue
                if ( abs(rect1.bbox[0] - rect2.bbox[0])
                      + abs(rect1.bbox[2] - rect2.bbox[2])
                      < 0.01 * rect1.bbox[0] ) :
                    if rect2.col < rect1.col:
                        #print "\t1:", rect2, "to", rect1
                        rect2.col = rect1.col
                elif (rect2.orphan and rect2.col < rect1.col
                        and rect2.bbox[0] >= rect1.bbox[0]
                        and rect2.bbox[2] <= rect1.bbox[2]):
                    #print "\t2:", rect2, "to", rect1
                    rect2.col = rect1.col


    @classmethod
    def assign_locations(cls):
        if cls._is_assigned:
            return
        cls._eliminate_dups()
        cls._assign_rows()
        cls._assign_cols()
        cls._check_cols()
        cls._is_assigned = True

    @classmethod
    def get_location(cls, cent):
        cls.assign_locations()
        rect = cls.find_rect(cent)
        if rect is None:
            return None, None
        return rect.row, rect.col


class Text(Element):
    _textlist = []
    _is_assigned = False

    def __init__(self, bbox, text):
        Element.__init__(self, bbox)
        self.text = text
        self.rect = None
        Text._textlist.append(self)
        Text._is_assigned = False

    def __unicode__(self):
        return (u"Text[%s, %s]: (%s) '%s'"
                % (self.row, self.col, self.cent, self.text))

    @classmethod
    def clear(cls):
        cls._textlist = []
        cls._is_assigned = False

    @classmethod
    def assign_locations(cls):
        if cls._is_assigned:
            return

        # assign each Text to a Rect
        # this can introduce new Rect and Text objects
        cls._assign_rect()

        # assign locations to text
        Rect.assign_locations() # assign a row/col to each rect
        for text in cls._textlist:
            text.row, text.col = Rect.get_location(text.cent)
            #print text

    @classmethod
    def _assign_rect(cls):
        # find orphans and create Rect objects from their bboxs
        for text in cls._textlist:
            text.rect = Rect.find_rect(text.cent)

            if text.rect is None:
                #print "Orphan text:", text
                text.rect = Rect(text.bbox)
                text.orphan = True
                text.rect.orphan = True

        # find text spanning rects
        # This occurs when adjacent cells are right and left justified
        # respectively.  That means a number followed  by text.
        # Make separare text item of leading number.
        split_text_objects = []
        for i_, text in enumerate(cls._textlist):
            if (text.bbox[0] >= (text.rect.bbox[0] -2) and
                text.bbox[2] <= (text.rect.bbox[2] +2) ):
                continue
            #Any text not passing the above test spans multiple rects.

            # If we can split the text and find Rects for the two parts
            # We will create two new Text objects and delete the old one
            #print "Splitting:", text
            fl = re.split(r'([-+]?[0-9]*\.?[0-9]+)', text.text, 1)
            if len(fl) == 3:
                text0 = fl[1]
                text1 = fl[2]
                cent0 = text.bbox[0], text.cent[1]
                cent1 = text.bbox[2], text.cent[1]
                rect0 = Rect.find_rect(cent0)
                rect1 = Rect.find_rect(cent1)
                if rect0 and rect1:
                    #print "\tSplit '%s' & '%s'."%(text0, text1)
                    t0 = Text((text.bbox[0], text.bbox[1],
                               rect0.bbox[2], rect0.bbox[3]),
                              text0)
                    t0.rect = rect0
                    t1 = Text((rect1.bbox[0], rect1.bbox[1],
                               text.bbox[2], text.bbox[3]),
                              text1)
                    t1.rect = rect1
                    split_text_objects.append(i_)
        split_text_objects.reverse()
        for i_ in split_text_objects: del cls._textlist[i_]


    @classmethod
    def get_row_text(cls, row):
        rowlist = [t for t in cls._textlist if t.row == row]
        rowlist.sort(key=lambda t:t.cent[1])
        rowlist.sort(key=lambda t:t.col)
        #print 'rowlist %s: %s'%row, rowlist
        col = 0
        coltext = ['']
        rowtext = []
        for text in rowlist:
            while text.col > col:
                rowtext.append(coltext)
                coltext = ['']
                col += 1
            coltext.append(text.text)
        rowtext.append(coltext)
        #print "Rowtext %s:"%row, rowtext
        return rowtext


class Sheet2 (object):
    def __init__(self):
        Rect.clear()
        Text.clear()

    def add_ltcontainer (self, obj, page_y_offset):
        #NB: row indexes (y axis) are negative!
        bbox = (obj.x0, -(obj.y1 + page_y_offset),
                obj.x1, -(obj.y0 + page_y_offset))

        if isinstance (obj, LTTextLine):
            txt = unicode(obj.get_text().strip())
            #print \
            Text(bbox, txt)
        elif isinstance (obj, LTRect):
            #print \
            Rect(bbox)
        elif isinstance (obj, LTContainer):
            for child in obj:
                self.add_ltcontainer (child, page_y_offset)
        else:
            pass

    def extract_rows (self):
        Text.assign_locations()
        rows = []
        for row in range(Rect.num_rows):
            rowtext = Text.get_row_text(row)
            joined_cols = [' '.join(c).strip() for c in rowtext]
            rows.append(joined_cols)
        return rows

