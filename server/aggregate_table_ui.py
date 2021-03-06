from mako.template import Template
from mako.lookup import TemplateLookup
import cherrypy
from aggregate_json_ui import json_aggregate_item, parse_kwargs
import os
from urllib import urlencode
import database as db


class AggregatePages(object):
    @cherrypy.expose
    def index(self):
        return self.callstacks()
    
    templates_dir = os.path.join(os.getcwd(),'static','templates')
    template_lookup = TemplateLookup(directories=[templates_dir,])

    @cherrypy.expose
    def callstacks(self, id=None, **kwargs):
        table_kwargs, filter_kwargs = parse_kwargs(kwargs)
        if 'id' in filter_kwargs:
            filter_kwargs.pop('id')
        for k in filter_kwargs:
            filter_kwargs[k] = str(filter_kwargs[k])
        
        if id:
            call_stack, total, filtered = json_aggregate_item(db.CallStack, filter_kwargs, id)

            if call_stack == None:
                raise cherrypy.HTTPError(404)

            call_stack[1] = str(call_stack[1]) #unicode throws off template when casting dict as js obj
            call_stack[2] = int(call_stack[2]) #convert long to int

            mytemplate = Template(filename=os.path.join(self.templates_dir,'aggregatecallstack.html'), lookup=self.template_lookup)
            return mytemplate.render(call_stack=call_stack, kwargs=filter_kwargs)
        else:
            mytemplate = Template(filename=os.path.join(self.templates_dir,'aggregatecallstacks.html'), lookup=self.template_lookup)
            return mytemplate.render(kwargs=filter_kwargs)

    @cherrypy.expose
    def sqlstatements(self, id=None, **kwargs):
        table_kwargs, filter_kwargs = parse_kwargs(kwargs)
        if 'id' in filter_kwargs:
            filter_kwargs.pop('id')
        for k in filter_kwargs:
            filter_kwargs[k] = str(filter_kwargs[k])
        
        if id:
            statement, total, filtered = json_aggregate_item(db.SQLStatement, filter_kwargs, id)

            if statement == None:
                raise cherrypy.HTTPError(404)

            statement[1] = str(statement[1]) #unicode throws off template when casting dict as js obj
            statement[2] = int(statement[2]) #convert long to int
            
            mytemplate = Template(filename=os.path.join(self.templates_dir,'aggregatesql.html'), lookup=self.template_lookup)
            return mytemplate.render(statement=statement, kwargs=filter_kwargs)
        else:
            
            mytemplate = Template(filename=os.path.join(self.templates_dir,'aggregatesqls.html'), lookup=self.template_lookup)
            return mytemplate.render(kwargs=filter_kwargs)

    @cherrypy.expose
    def fileaccesses(self, id=None, **kwargs):
        table_kwargs, filter_kwargs = parse_kwargs(kwargs)
        if 'id' in filter_kwargs:
            filter_kwargs.pop('id')
        for k in filter_kwargs:
            filter_kwargs[k] = str(filter_kwargs[k])
        
        if id:
            file_access, total, filtered = json_aggregate_item(db.FileAccess, filter_kwargs, id)

            if file_access == None:
                raise cherrypy.HTTPError(404)

            file_access[1] = str(file_access[1]) #unicode throws off template when casting dict as js obj
            file_access[2] = int(file_access[2]) #convert long to int
            
            mytemplate = Template(filename=os.path.join(self.templates_dir,'aggregatefileaccess.html'), lookup=self.template_lookup)
            return mytemplate.render(file_access=file_access, kwargs=filter_kwargs)
        else:
            
            mytemplate = Template(filename=os.path.join(self.templates_dir,'aggregatefileaccesses.html'), lookup=self.template_lookup)
            return mytemplate.render(kwargs=filter_kwargs)
