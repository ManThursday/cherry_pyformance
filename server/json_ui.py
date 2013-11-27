# import sqlalchemy
import database as db
import cherrypy
# from sqlalchemy import or_, and_
# from cgi import escape as html_escape


class JSONAPI(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def callstacks(self, id=None, **kwargs):
        if id:
            item = db.session.query(db.CallStack).get(id)
            if item:
                response = item._to_dict()
                response['stack'] = item._stack()
                return response
            else:
                raise cherrypy.NotFound
        else:
            results = db.session.query(db.CallStack)
            return [item._to_dict() for item in results.all()]


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def callstackitems(self, id=None, **kwargs):
        if id:
            return db.session.query(db.CallStackItem).get(id)._to_dict()
        else:
            results = db.session.query(db.CallStackItem)
            return [item._to_dict() for item in results.all()]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def sqlstatements(self, id=None, **kwargs):
        if id:
            item = db.session.query(db.SQLStatement).get(id)
            if item:
                response = item._to_dict()
                response['stack'] = item._stack()
                return response
            else:
                raise cherrypy.NotFound
        else:
            results = db.session.query(db.SQLStatement)
            return [item._to_dict() for item in results.all()]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def sqlstackitems(self, id=None, **kwargs):
        if id:
            return db.session.query(db.SQLStackItem).get(id)._to_dict()
        else:
            results = db.session.query(db.SQLStackItem)
            return [item._to_dict() for item in results.all()]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def fileaccesses(self, id=None, **kwargs):
        if id:
            return db.session.query(db.FileAccess).get(id)._to_dict()
        else:
            results = db.session.query(db.FileAccess)
            return [item._to_dict() for item in results.all()]


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def metadata(self, id=None, **kwargs):
        main_table_item = None
        if 'get_keys' in kwargs:
            key_list_dicts = db.session.query(db.MetaData.key).distinct().all()
            return [key_dict[0] for key_dict in key_list_dicts]
        elif 'call_stack_id' in kwargs:
            main_table_item = db.session.query(db.CallStack).get(kwargs['call_stack_id'])
        elif 'sql_statement_id' in kwargs:
            main_table_item = db.session.query(db.SQLStatement).get(kwargs['sql_statement_id'])
        elif 'file_access_id' in kwargs:
            main_table_item = db.session.query(db.FileAccess).get(kwargs['file_access_id'])
        
        data = []
        if main_table_item:
            for metadata in main_table_item.metadata_items:
                record = [html_escape(str(metadata.__dict__[x])) for x in ['id','key','value']]
                data.append(record)
        else:
            metadata_list = db.session.query(db.MetaData).filter_by(**kwargs).all()
            for metadata in metadata_list:
                value = html_escape(str(metadata.__dict__['value']))
                data.append(value)
            data.sort(key=str.lower)
        
        return {'aaData':data}
