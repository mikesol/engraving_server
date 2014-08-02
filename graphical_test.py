import tuplet_to_factor
import rhythmic_events_to_durations
import clef_to_width
import key_signature_to_width
import time_signature_to_width
import accidental_to_width
import dots_to_width
import rhythmic_events_to_right_width
import rhythmic_events_to_left_width
import nexts_to_graphical_next
import graphical_next_to_space_prev
import space_prev_to_x_position
import duration_log_to_width

import emmentaler_tools

import time

from plain import *
from properties import *
from sqlalchemy import create_engine
from sqlalchemy import event, DDL


LOG = True
ECHO = True
#ECHO = False
MANUAL_DDL = False
#MANUAL_DDL = True
#engine = create_engine('postgresql://localhost/postgres', echo=False)
engine = create_engine('sqlite:///memory', echo=ECHO)
conn = engine.connect()

generate_sqlite_functions(conn)

manager = DDL_manager()
###############################
manager.ddls += tuplet_to_factor.generate_ddl(name = Name,
                    left_bound = Left_bound,
                    right_bound = Right_bound,
                    time_next = Time_next,
                    tuplet_fraction = Tuplet_fraction,
                    tuplet_factor = Tuplet_factor)
###############################
manager.ddls += rhythmic_events_to_durations.generate_ddl(duration_log = Duration_log,
                    dots = Dots,
                    tuplet_factor = Tuplet_factor,
                    duration = Duration)

manager.ddls += key_signature_to_width.generate_ddl(name = Name,
                                     font_name = Font_name,
                                     font_size = Font_size,
                                     key_signature = Key_signature,
                                     glyph_box = Glyph_box,
                                     width = Width)

###############################
manager.ddls += clef_to_width.generate_ddl(name = Name,
                                   font_name = Font_name,
                                   font_size = Font_size,
                                   glyph_idx = Glyph_idx,
                                   glyph_box = Glyph_box,
                                   width = Width)

###############################
manager.ddls += time_signature_to_width.generate_ddl(name = Name,
                                     font_name = Font_name,
                                     font_size = Font_size,
                                     time_signature = Time_signature,
                                     string_box = String_box,
                                     width = Width)

###############################
manager.ddls += accidental_to_width.generate_ddl(font_name = Font_name,
                                     font_size = Font_size,
                                     accidental = Accidental,
                                     glyph_box = Glyph_box,
                                     accidental_width = Accidental_width)

################################
manager.ddls += duration_log_to_width.generate_ddl(font_name = Font_name,
                                     font_size = Font_size,
                                     duration_log = Duration_log,
                                     glyph_box = Glyph_box,
                                     name = Name,
                                     rhythmic_event_width = Rhythmic_event_width)

###############################
manager.ddls += dots_to_width.generate_ddl(font_name = Font_name,
                                     font_size = Font_size,
                                     dots = Dots,
                                     glyph_box = Glyph_box,
                                     dot_padding = Dot_padding,
                                     dot_width = Dot_width)


###############################
manager.ddls += rhythmic_events_to_right_width.generate_ddl(glyph_box = Glyph_box,
                                     rhythmic_event_width = Rhythmic_event_width,
                                     dot_width = Dot_width,
                                     rhythmic_event_to_dot_padding = Rhythmic_event_to_dot_padding,
                                     right_width = Right_width)

###############################
manager.ddls += rhythmic_events_to_left_width.generate_ddl(glyph_box = Glyph_box,
                                     rhythmic_event_width = Rhythmic_event_width,
                                     accidental_width = Accidental_width,
                                     rhythmic_event_to_accidental_padding = Rhythmic_event_to_accidental_padding,
                                     left_width = Left_width)

###############################
manager.ddls += nexts_to_graphical_next.generate_ddl(horstemps_anchor = Horstemps_anchor,
                                     horstemps_next = Horstemps_next,
                                     time_next = Time_next,
                                     graphical_next = Graphical_next)

###############################
manager.ddls += graphical_next_to_space_prev.generate_ddl(graphical_next = Graphical_next,
                                     name = Name,
                                     width = Width,
                                     left_width = Left_width,
                                     right_width = Right_width,
                                     duration = Duration,
                                     space_prev = Space_prev)

###############################
manager.ddls += space_prev_to_x_position.generate_ddl(graphical_next = Graphical_next,
                                     space_prev = Space_prev,
                                     x_position = X_position)
if not MANUAL_DDL :
  manager.register_ddls(conn, LOG = True)

Score.metadata.drop_all(engine)
Score.metadata.create_all(engine)

emmentaler_tools.populate_glyph_box_table(conn, Glyph_box)
emmentaler_tools.add_to_string_box_table(conn, String_box, '3')
emmentaler_tools.add_to_string_box_table(conn, String_box, '4')

stmts = []

# DEFAULTS
# TODO - in separate file?
stmts.append((Dot_padding, {'id': -1, 'val':0.1}))
stmts.append((Rhythmic_event_to_dot_padding, {'id':-1, 'val': 0.1}))
stmts.append((Rhythmic_event_to_accidental_padding, {'id':-1, 'val': 0.1}))

# link up notes in time
TN = [3,4,5,7,8,None]
for x in range(len(TN) - 1) :
  stmts.append((Time_next, {'id':TN[x], 'val':TN[x+1]}))

# A time signature
stmts.append((Name, {'id':0,'val':'time_signature'}))
stmts.append((Font_name, {'id':0,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':0,'val':20}))
stmts.append((Time_signature, {'id':0,'num':3,'den':4}))

# A key signature
stmts.append((Name, {'id':1,'val':'key_signature'}))
stmts.append((Font_name, {'id':1,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':1,'val':20}))
stmts.append((Key_signature, {'id':1,'val':2}))

# A clef
stmts.append((Name, {'id':2,'val':'clef'}))
stmts.append((Font_name, {'id':2,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':2,'val':20}))
stmts.append((Glyph_idx, {'id':2,'val':116}))

# some notes and rests
stmts.append((Name, {'id':3,'val':'note'}))
stmts.append((Font_name, {'id':3,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':3,'val':20}))
stmts.append((Duration_log, {'id':3,'val':-2}))
stmts.append((Dots, {'id':3,'val':1}))
stmts.append((Accidental, {'id':3,'val':-1}))

stmts.append((Name, {'id':4,'val':'rest'}))
stmts.append((Font_name, {'id':4,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':4,'val':20}))
stmts.append((Duration_log, {'id':4,'val':-1}))
stmts.append((Dots, {'id':4,'val':2}))

stmts.append((Name, {'id':5,'val':'note'}))
stmts.append((Font_name, {'id':5,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':5,'val':20}))
stmts.append((Duration_log, {'id':5,'val':0}))

# another clef
stmts.append((Name, {'id':6,'val':'clef'}))
stmts.append((Font_name, {'id':6,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':6,'val':20}))
stmts.append((Glyph_idx, {'id':6,'val':116}))

# some notes and rests
stmts.append((Name, {'id':7,'val':'note'}))
stmts.append((Font_name, {'id':7,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':7,'val':20}))
stmts.append((Duration_log, {'id':7,'val':-3}))
stmts.append((Dots, {'id':7,'val':2}))
stmts.append((Accidental, {'id':7,'val':1}))

stmts.append((Name, {'id':8,'val':'rest'}))
stmts.append((Font_name, {'id':8,'val':'emmentaler-20'}))
stmts.append((Font_size, {'id':8,'val':20}))
stmts.append((Duration_log, {'id':8,'val':-1}))

# link up things out of time, including to their anchors
# link up notes in time
HT_0 = [0,1,2,None]
for x in range(len(HT_0) - 1) :
  stmts.append((Horstemps_next, {'id':HT_0[x], 'val':HT_0[x+1]}))
  stmts.append((Horstemps_anchor, {'id':HT_0[x], 'val':3}))

HT_1 = [6,None]
for x in range(len(HT_1) - 1) :
  stmts.append((Horstemps_next, {'id':HT_1[x], 'val':HT_1[x+1]}))
  stmts.append((Horstemps_anchor, {'id':HT_1[x], 'val':7}))

# run!

trans = conn.begin()
for st in stmts :
  print "~~~~~~~~~~~~~~~~~~~~~~~", st[0].name, st[1]
  manager.insert(conn, st[0].insert().values(**st[1]), MANUAL_DDL)
trans.commit()

NOW = time.time()
for row in conn.execute(select([X_position])).fetchall() :
  print row