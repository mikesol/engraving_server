from sqlalchemy.sql.expression import literal, distinct, exists, text, case
from core_tools import *
import time
import bravura_tools

class _Delete(DeleteStmt) :
  def __init__(self, rhythmic_event_dimension) :
    def where_clause_fn(id) :
      return rhythmic_event_dimension.c.id == id
    DeleteStmt.__init__(self, rhythmic_event_dimension, where_clause_fn)

class _Insert(InsertStmt) :
  def __init__(self, font_name, font_size, duration_log, glyph_box, name, rhythmic_event_dimension, dimension) :
    InsertStmt.__init__(self)
    self.font_name = font_name
    self.font_size = font_size
    self.duration_log = duration_log
    self.glyph_box = glyph_box
    self.name = name
    self.rhythmic_event_dimension = rhythmic_event_dimension
    self.dimension = dimension

  def _generate_stmt(self, id) :
    font_name = self.font_name
    font_size = self.font_size
    duration_log = self.duration_log
    glyph_box = self.glyph_box
    name = self.name
    rhythmic_event_dimension = self.rhythmic_event_dimension
    dimension = self.dimension

    duration_log_to_rhythmic_event_dimensions = select([
      duration_log.c.id.label('id'),
      (glyph_box.c[dimension] * font_size.c.val / 20.0).label('val')
    ]).select_from(duration_log.join(font_name, onclause = duration_log.c.id == font_name.c.id).\
                   join(name, onclause = duration_log.c.id == name.c.id).\
                   join(font_size, onclause = duration_log.c.id == font_size.c.id).\
                   join(glyph_box, onclause = font_name.c.val == glyph_box.c.name)).\
          where(safe_eq_comp(duration_log.c.id, id)).\
          where(
             and_(glyph_box.c.unicode == case([(and_(duration_log.c.val == -1, name.c.val == 'note'), "U+E0A3"),
                                            (and_(duration_log.c.val == 0, name.c.val == 'note'), "U+E0A2"),
                                            (and_(duration_log.c.val == 0, name.c.val == 'rest'), "U+E4E3"),
                                            (and_(duration_log.c.val == -1, name.c.val == 'rest'), "U+E4E4"),
                                            (and_(duration_log.c.val == -2, name.c.val == 'rest'), "U+E4E5"),
                                            (and_(duration_log.c.val == -3, name.c.val == 'rest'), "U+E4E6"),
                                            (and_(duration_log.c.val == -4, name.c.val == 'rest'), "U+E4E7"),
                                            (and_(duration_log.c.val == -5, name.c.val == 'rest'), "U+E4E8"),
                                            (and_(duration_log.c.val == -6, name.c.val == 'rest'), "U+E4E9"),
                                            (and_(duration_log.c.val == -7, name.c.val == 'rest'), "U+E4EA"),
                                            (name.c.val == 'note', "U+E0A4")],
                                           else_ = 0))).\
    cte(name='duration_log_to_rhythmic_event_dimensions')

    self.register_stmt(duration_log_to_rhythmic_event_dimensions)

    self.insert = simple_insert(rhythmic_event_dimension, duration_log_to_rhythmic_event_dimensions)

def generate_ddl(font_name, font_size, duration_log, glyph_box, name, rhythmic_event_dimension, dimension) :
  OUT = []

  insert_stmt = _Insert(font_name, font_size, duration_log, glyph_box, name, rhythmic_event_dimension, dimension)

  del_stmt = _Delete(rhythmic_event_dimension)
  
  when = EasyWhen(font_name, duration_log, name)

  OUT += [DDL_unit(table, action, [del_stmt], [insert_stmt], when_clause = when)
     for action in ['INSERT', 'UPDATE', 'DELETE']
     for table in [font_name, duration_log, name]]

  return OUT

if __name__ == "__main__" :
  import math
  from properties import *
  from sqlalchemy import create_engine
  from sqlalchemy import event, DDL
  
  ECHO = False
  #MANUAL_DDL = True
  MANUAL_DDL = False
  #engine = create_engine('postgresql://localhost/postgres', echo=False)
  engine = create_engine('sqlite:///memory', echo=ECHO)
  conn = engine.connect()
  generate_sqlite_functions(conn)

  manager = DDL_manager(generate_ddl(font_name = Font_name,
                                     font_size = Font_size,
                                     duration_log = Duration_log,
                                     glyph_box = Glyph_box,
                                     name = Name,
                                     rhythmic_event_dimension = Rhythmic_head_width,
                                     dimension = 'width'))

  manager.ddls += generate_ddl(font_name = Font_name,
                                     font_size = Font_size,
                                     duration_log = Duration_log,
                                     glyph_box = Glyph_box,
                                     name = Name,
                                     rhythmic_event_dimension = Rhythmic_head_height,
                                     dimension = 'height')

  if not MANUAL_DDL :
    manager.register_ddls(conn, LOG = True)

  Score.metadata.drop_all(engine)
  Score.metadata.create_all(engine)

  bravura_tools.populate_glyph_box_table(conn, Glyph_box)

  stmts = []

  DL = [-4,-3,-2,-1,0]
  N = ['note', 'rest']
  for n in range(len(N)) :
    name = N[n]
    for x in range(len(DL)) :
      stmts.append((Font_name, {'id':x + (len(DL) * n),'val':'Bravura'}))
      stmts.append((Font_size, {'id':x + (len(DL) * n),'val':20}))
      stmts.append((Duration_log, {'id':x + (len(DL) * n),'val': DL[x]}))
      stmts.append((Name, {'id':x + (len(DL) * n),'val': name}))

  trans = conn.begin()
  for st in stmts :
    manager.insert(conn, st[0].insert().values(**st[1]), MANUAL_DDL)
  trans.commit()

  NOW = time.time()
  for row in conn.execute(select([Rhythmic_head_width])).fetchall() :
    print row

  print "*"*40
  
  for row in conn.execute(select([Rhythmic_head_height])).fetchall() :
    print row
  
  #manager.update(conn, Duration, {'num':100, 'den':1}, Duration.c.id == 4, MANUAL_DDL)
  
  #print "*************"
  #print time.time() - NOW
  #for row in conn.execute(select([Local_onset])).fetchall() :
  #  print row
