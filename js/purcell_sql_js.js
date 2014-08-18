// combine with other file...
purcell.sql_socket = {};
purcell.make_websocket = function(out) {
  purcell.$0cket = purcell.sql_socket;
  purcell.$0cket.db = new window.SQL.Database();
  purcell.$0cket.db.run(purcell.$0cket.PROGRAM);
  purcell.$0cket.send = function(json) {
    var data = JSON.parse(json);
    var sql = data.sql;
    var out = {}
    if (data.subsequent != null) {
      out.subsequent = data.subsequent;
    }
    if (sql != null) {
      for (var i = 0; i < sql.length; i++) {
        // we only take the first statement
        var evaluated_sql = purcell.$0cket.db.exec(sql[i]['sql']);
        if (evaluated_sql.length > 0) {
          evaluated_sql = evaluated_sql[0];
          var ret = [];
          for (var j = 0; j < evaluated_sql.values.length; j++) {
            ret.push({});
            for (var k = 0; k < evaluated_sql.values[j].length; k++) {
              ret[j][evaluated_sql.columns[k]] = evaluated_sql.values[j][k];
            }
          }
          var name = sql[i]['name'] ? sql[i]['name'] : 'anonymous';
          out[name] = ret;
        }
      }
    }
    evt = {}
    evt.data = JSON.stringify(out);
    purcell.$0cket.onmessage(evt);
  }
  purcell.$0cket.onmessage = function(evt) {
    json = eval("("+evt.data+")")
    var subsequent = json.subsequent;
    if (subsequent) {
      eval(subsequent+"("+evt.data+")");
    }
    purcell.CURRENT_DATA = evt.data;
  }
  out = {
         client:purcell.MY_NAME,
         initializing:true,
         sql:out,
         'return': 'just_me',
        };
  purcell.$0cket.send(JSON.stringify(out));
  out = [];
  purcell.append_standard_graphical_queries(out);
  out = {
         client:purcell.MY_NAME,
         sql:out,
         'return': 'everyone',
         subsequent:"purcell.draw"
        };
  purcell.$0cket.send(JSON.stringify(out));
}