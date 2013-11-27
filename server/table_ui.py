import mako.template
import sqlalchemy
import database as db
import cherrypy
import os
from urllib import urlencode

class Tables(object):

    @cherrypy.expose
    def callstacks(self, id=None, **kwargs):
        if id:
            call_stack = db.session.query(db.CallStack).get(id)
            if call_stack == None:
                raise cherrypy.HTTPError(404)
            metadata_list = call_stack.metadata_items
            metadata_id = None
            for metadata in metadata_list:
                if metadata.key == 'full_method':
                    metadata_id = metadata.id
                    break
            mytemplate = mako.template.Template(filename=os.path.join(os.getcwd(),'static','templates','callstack.html'))
            return mytemplate.render(call_stack=call_stack, metadata_id=metadata_id, encoded_kwargs=urlencode(kwargs))
        else:
            mytemplate = mako.template.Template(filename=os.path.join(os.getcwd(),'static','templates','callstacks.html'))
            return mytemplate.render(encoded_kwargs=urlencode(kwargs))

    @cherrypy.expose
    def sqlstatements(self, id=None, **kwargs):
        if id:
            sql_statement = db.session.query(db.SQLStatement).get(id)
            if sql_statement == None:
                raise cherrypy.HTTPError(404)
            metadata_list = sql_statement.metadata_items
            metadata_id = None
            for metadata in metadata_list:
                if metadata.key == 'sql_string':
                    metadata_id = metadata.id
                    break
            mytemplate = mako.template.Template(filename=os.path.join(os.getcwd(),'static','templates','sqlstatement.html'))
            return mytemplate.render(sql_statement=sql_statement, metadata_id=metadata_id, encoded_kwargs=urlencode(kwargs))
        else:
            mytemplate = mako.template.Template(filename=os.path.join(os.getcwd(),'static','templates','sqlstatements.html'))
            return mytemplate.render(encoded_kwargs=urlencode(kwargs))

    @cherrypy.expose
    def fileaccesses(self, id=None, **kwargs):
        if id:
            file_access = db.session.query(db.FileAccess).get(id)
            if file_access == None:
                raise cherrypy.HTTPError(404)
            metadata_list = file_access.metadata_items
            metadata_id = None
            for metadata in metadata_list:
                if metadata.key == 'filename':
                    metadata_id = metadata.id
                    break
            mytemplate = mako.template.Template(filename=os.path.join(os.getcwd(),'static','templates','fileaccess.html'))
            return mytemplate.render(file_access=file_access, metadata_id=metadata_id, encoded_kwargs=urlencode(kwargs))
        else:
            mytemplate = mako.template.Template(filename=os.path.join(os.getcwd(),'static','templates','fileaccesses.html'))
            return mytemplate.render(encoded_kwargs=urlencode(kwargs))