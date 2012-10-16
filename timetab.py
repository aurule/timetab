# CORE FEATURES
# data comes in via file
# once we know how much space our timeline has, we can start splitting it up
#   since we're working with the svg format, absolute distances doesn't matter as much, but it's still important for scaling, etc.
# we also need hard start and end dates (times too?), so that we can do relative calculations
#   other methods might only require a hard start date, by requiring a pixels/day definition instead of an end date
#   time field is used to display multiple events per date, but not multiple markers
# each event's date must be reduced to the number of days since the start of the graph
# then, that's translated into pixels to get the X coordinate of the event

# VERSION 2
# support fine-grained placement by time as well as date
# predefined label formats
#   labels should be able to include the date
# wider input support
#   take an end date and calculate backwards
# support events which span multiple units of time

# VERSION 3
# gui!

import ConfigParser
import csv
import sys
from datetime import datetime
import argparse

def mkline(formula, line_id):
    out = '<path style="fill:none;stroke:#000000;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" d="'+formula+'" id="'+line_id+'" inkscape:connector-curvature="0" />'
    return out
def mktext(cox, coy, text, text_id):
    out = '<text xml:space="preserve" style="font-size:8px;font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:DejaVu Serif;-inkscape-font-specification:DejaVu Serif" x="'+str(cox)+'" y="'+str(coy)+'" id="'+text_id+'" sodipodi:linespacing="125%"><tspan sodipodi:role="line" id="tspan2989" x="266.68027" y="-80.018814">'+text+'</tspan></text>'
    return out

parser = argparse.ArgumentParser(description="Create a timeline svg.") #TODO add a full description description
parser.add_argument('--ofile', '-o', action='store', default='-', metavar='filename', help='output file for the timeline (SVG formatted)')
parser.add_argument('ini', action='store', metavar='config_file', help='configuration file for the timeline in INI format')
parser.add_argument('data', action='store', metavar='data_file', nargs='+', help='data file for the timeline in CSV format')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.01')
args = parser.parse_args()

config = ConfigParser.RawConfigParser()
config.read(args.ini)

#parse and store config options
#required: length, start, end
length = float(config.get('plot', 'length'))
start_date = datetime.strptime(config.get('plot', 'start'), '%Y-%m-%d')
end_date = datetime.strptime(config.get('plot', 'end'), '%Y-%m-%d')
delta = end_date - start_date
totaldays = float(delta.days)
#optional: title, others?
title = config.get('plot', 'title')
print """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="1000"
   height="100"
   id="svg2"
   version="1.1"
   inkscape:version="0.48.2 r9819"
   sodipodi:docname="New document 1">
  <defs
     id="defs4" />
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="1"
     inkscape:cx="348.34819"
     inkscape:cy="736.39975"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1440"
     inkscape:window-height="876"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
"""

idctr = 0
print mkline("m 0,90 "+str(length)+",0", 'baseline')

for marker in [1600, 1700, 1800, 1900, 2000, 2010]:
    mdate = datetime.strptime(str(marker), '%Y')
    delta = mdate - start_date
    daydiff = float(delta.days)
    pos = (daydiff / totaldays) * length
    
    idctr += 1
    print mkline("m "+str(pos)+",95 0,-10", 'line_'+str(idctr))
    print mktext(pos-10, 105, str(mdate), 'text_'+str(idctr))
    

#read each data file and add its entries to the timeline
for fname in args.data:
    data = csv.reader(open(fname, 'rb'))
    headers = data.next()
    #find row position values for "event" and "date"
    datecol = headers.index('date')
    eventcol = headers.index('event')
    
    for row in data:
        rdate = row[datecol]
        rtag = row[eventcol]
        event_date = datetime.strptime(rdate, '%m/%d/%Y')
        delta = event_date - start_date
        daydiff = float(delta.days)
        pos = (daydiff / totaldays) * length
        
        idctr += 1
        print mkline("m "+str(pos)+",80 0,10 30,60", 'line_'+str(idctr))
        print mktext(pos+32, 23, rdate+': '+rtag, 'text_'+str(idctr))
        #TODO prevent collisions? no idea

print "</g></svg>"
