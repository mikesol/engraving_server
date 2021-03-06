from sqlalchemy import Integer, Float, String, Column
from core_tools import make_table, make_table_generic, Fraction, Spanner, Box, Point
import core_tools

Score = make_table('score', Integer)
Staff = make_table('staff', Integer)
Voice = make_table('voice', Integer)

### prime tables

# name of the thing (chord, tuplet, etc.)
Name = make_table('name', String(50))

# note to containing chord
Chord = make_table('chord', Integer)
# 2**duration_log is the base length of the note
Duration_log = make_table('duration_log', Integer)
# dots to a note
Dots = make_table('dots', Integer)
# the next chord, rest, or space in a sequence
Time_next = make_table('time_next', Integer, unique=True)
# the anchor for time next strands
Onset_anchor = make_table('onset_anchor', Integer)

# accidental attached to a note
Accidental = make_table('accidental', Integer)
# pitch attached to a note
Pitch = make_table('pitch', Integer)
# octave attached to a note
Octave = make_table('octave', Integer)

# beam that a stem belongs to
Beam = make_table('beam', Integer)

# the fraction of a tuplet
Tuplet_fraction = make_table('tuplet_fraction', Fraction)

# time signature num den
Time_signature = make_table('time_signature', Fraction)

# key signature where +1 is G Major, -4 A-flat major, etc...
Key_signature = make_table('key_signature', Integer)

# the staff symbol that something is on
Staff_symbol = make_table('staff_symbol', Integer)

# position of object on staff
Staff_position = make_table('staff_position', Float)

### derived tables

# the full duration of an event
#Duration = make_table('duration', Fraction)
Duration = make_table('duration', Float)

# the onset of an event
Local_onset = make_table('local_onset', Fraction)
# the event in a sequence that is anchored to another sequence
Onset_referent = make_table('onset_referent', Integer)
# the global onset in the piece
Global_onset = make_table('global_onset', Fraction)

# layout
Dot_padding = make_table('dot_padding', Float)
Rhythmic_event_to_dot_padding = make_table('rhythmic_event_to_dot_padding', Float)
Rhythmic_event_to_accidental_padding = make_table('rhythmic_event_to_accidental_padding', Float)
Time_signature_inter_number_padding = make_table('time_signature_inter_number_padding', Float)
Key_signature_inter_accidental_padding = make_table('key_signature_inter_accidental_padding', Float)

Left_tuplet_bound = make_table('left_tuplet_bound', Integer)
Right_tuplet_bound = make_table('right_tuplet_bound', Integer)
Tuplet_factor = make_table('tuplet_factor', Fraction)

Horstemps_next = make_table('horstemps_next', Integer, unique=True)
Horstemps_anchor = make_table('horstemps_anchor', Integer)

Font_name = make_table('font_name', String)
Font_size = make_table('font_size', Float)
Unicode = make_table('unicode', Integer)

# has a ledger line?
Ledger_line = make_table('ledger_line', Integer)

Bar_thickness = make_table('bar_thickness', Integer)

# length of stems
Stem_length = make_table('stem_length', Float)
Natural_stem_direction = make_table('natural_stem_direction', Integer)
Stem_direction = make_table('stem_direction', Integer)
Stem_x_offset = make_table('stem_x_offset', Float)
Natural_stem_end = make_table('natural_stem_end', Float)
Stem_end = make_table('stem_end', Float)

Beam_x_position = make_table('beam_x_position', Spanner)
Beam_y_position = make_table('beam_y_position', Spanner)

Anchor = make_table('anchor', Integer)
Anchor_x = make_table('anchor_x', Integer)
Anchor_y = make_table('anchor_y', Integer)

Rhythmic_head_width = make_table('rhythmic_head_width', Float)
Rhythmic_head_height = make_table('rhythmic_head_height', Float)
Dot_width = make_table('dot_width', Float)
Accidental_width = make_table('accidental_width', Float)
Left_width = make_table('left_width', Float)
Right_width = make_table('right_width', Float)
Note_box = make_table('note_box', Box)

Dynamic_padding = make_table('dynamic_padding', Float)
Dynamic = make_table('dynamic', String)
Dynamic_direction = make_table('dynamic_direction', Integer)
Dynamic_staff_position = make_table('dynamic_staff_position', Float)

Width = make_table('width', Float)
Height = make_table('height', Float)

Space_prev = make_table_generic('space_prev',
  [Column('id', Integer, primary_key=True, index=core_tools._GLOBAL_INDEX),
   Column('prev',Integer), Column('val',Float, index=core_tools._GLOBAL_INDEX),])

Alignment_directive = make_table('alignment_directive', Point)
X_position = make_table('x_position', Float)
Y_position = make_table('y_position', Float)
Anchored_x_position = make_table('anchored_x_position', Float)
Anchored_y_position = make_table('anchored_y_position', Float)

Graphical_next = make_table_generic('graphical_next', [
      Column('id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
      Column('prev', Integer, unique = True, index=core_tools._GLOBAL_INDEX),
      Column('next', Integer, unique = True, index=core_tools._GLOBAL_INDEX)])

Line_thickness = make_table('line_thickness', Float)
Line_stencil = make_table_generic('line_stencil', [
                     Column('id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('writer', String, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('sub_id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('x0', Float, index=core_tools._GLOBAL_INDEX),
                     Column('y0', Float, index=core_tools._GLOBAL_INDEX),
                     Column('x1', Float, index=core_tools._GLOBAL_INDEX),
                     Column('y1', Float, index=core_tools._GLOBAL_INDEX),
                     Column('thickness', Float, index=core_tools._GLOBAL_INDEX)])

# Staff symbol
N_lines = make_table('n_lines', Integer)
Staff_space = make_table('staff_space', Float)

Glyph_stencil = make_table_generic('glyph_stencil', [Column('id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('writer', String, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('sub_id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('font_name', String, index=core_tools._GLOBAL_INDEX),
                     Column('font_size', Float, index=core_tools._GLOBAL_INDEX),
                     Column('unicode', String, index=core_tools._GLOBAL_INDEX),
                     Column('x', Float, index=core_tools._GLOBAL_INDEX),
                     Column('y', Float, index=core_tools._GLOBAL_INDEX)])

Polygon_stencil = make_table_generic('polygon_stencil', [Column('id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('writer', String, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('sub_id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('point', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('x', Float, index=core_tools._GLOBAL_INDEX),
                     Column('y', Float, index=core_tools._GLOBAL_INDEX),
                     Column('thickness', Float, index=core_tools._GLOBAL_INDEX),
                     Column('fill', Integer, index=core_tools._GLOBAL_INDEX),
                     Column('stroke', Integer, index=core_tools._GLOBAL_INDEX),
                     ])

String_stencil = make_table_generic('string_stencil', [Column('id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('writer', String, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('sub_id', Integer, primary_key = True, index=core_tools._GLOBAL_INDEX),
                     Column('font_name', String, index=core_tools._GLOBAL_INDEX),
                     Column('font_size', Float, index=core_tools._GLOBAL_INDEX),
                     Column('str', String, index=core_tools._GLOBAL_INDEX),
                     Column('x', Float, index=core_tools._GLOBAL_INDEX),
                     Column('y', Float, index=core_tools._GLOBAL_INDEX)
])