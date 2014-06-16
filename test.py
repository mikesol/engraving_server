from sqlalchemy import MetaData, create_engine, asc, desc, insert, update, select, and_, delete, case
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateTable
from blackmagick import BlackMagick

#&&&&&&&&&&&&&&&#
engine = create_engine('sqlite:///:memory:', echo=False)
conn = engine.connect()

_13 = BlackMagick()
_13.metadata = MetaData()
_13.session = sessionmaker()(bind=conn)
#&&&&&&&&&&&&&&&#

SQL = {}
import document_properties
SQL['properties'] = document_properties.P(_13)
SQL['counter'] = _13.make_counter()

#&&&&&&&&&&&&&&&#

#&&&&&&&&&&&&&&&#
#&&&&&&&&&&&&&&&#

SQL['engravers'] = []
####################################
import first_clef_on_staves
SQL['engravers'].append(first_clef_on_staves.E(_13))

import end_to_durations
SQL['engravers'].append(end_to_durations.E(_13))

import duration_log_to_notes
SQL['engravers'].append(duration_log_to_notes.E(_13))

import glyph_index_to_notes
SQL['engravers'].append(glyph_index_to_notes.E(_13))

########################################
##########################################
############################################
# Logic
# first, create tables
for PROPERTY in SQL['properties'] :
  engine.execute(CreateTable(PROPERTY))

#&&&&&&&&&&&&&&&#
# then, create_a_score
INSERTS = []
INSERTS += [_13.Score(id=x+1, val=0) for x in range(8)]
INSERTS += [_13.Staff(id=x+1, val=x%2) for x in range(8)]
INSERTS += [_13.Duration(id=x+1, num=1, den=4) for x in range(8)]
INSERTS += [_13.Onset(id=x+1, num=x/2, den=4) for x in range(8)]
INSERTS += [_13.Name(id=x+1, val="note") for x in range(8)]
INSERTS += [_13.Pointer(id=x+1, source=None) for x in range(8)]

for x in INSERTS :
  _13.session.add(x)
_13.session.commit()

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
# then, create engravers

for ENGRAVER in SQL['engravers'] :
  for TABLE in ENGRAVER.get('tables', []) :
    engine.execute(CreateTable(TABLE))

#@^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^@#
# then, run engravers until there are no more changes
LAST = -1
CUR = conn.execute(SQL['counter']).fetchall()[0][0]

while LAST != CUR :
  LAST = CUR
  for ENGRAVER in SQL['engravers'] :
    for elt in ENGRAVER.get('inserter', []) :
      conn.execute(elt)
    for elt in ENGRAVER.get('pointer', []) :
      conn.execute(elt)
    for elt in ENGRAVER.get('updater', []) :
      conn.execute(elt)
  CUR = conn.execute(SQL['counter']).fetchall()[0][0]

for row in conn.execute(select([_13.t(_13.Glyph_index)])).fetchall() :
  print row
