from smart.models.rdf_store import *
from smart.models.records import *
from smart.lib.utils import *

import re

def record_get_object(request, record_id, obj,  **kwargs):
    c = RecordStoreConnector(Record.objects.get(id=record_id))
    id = smart_path(request.path)                
    if ('external_id' in kwargs):
        id = obj.internal_id(c, kwargs['external_id'])
        assert (id != None), "No %s was found with external_id %s"%(obj.type, kwargs['external_id'])
    
    return rdf_get(c, obj.query_one("<%s>"%id.encode()))

def record_delete_object(request,  record_id, obj, **kwargs):
    c = RecordStoreConnector(Record.objects.get(id=record_id))
    id = smart_path(request.path)                
    if ('external_id' in kwargs):            
        id = obj.internal_id(c, kwargs['external_id'])
        assert (id != None), "No %s was found with external_id %s"%(obj.type, kwargs['external_id'])
    return rdf_delete(c, obj.query_one("<%s>"%id.encode()))

def record_get_all_objects(request, record_id, obj, **kwargs):
    c = RecordStoreConnector(Record.objects.get(id=record_id))
    return rdf_get(c, obj.query_all())

def record_delete_all_objects(request, record_id, obj, **kwargs):
    
    c = RecordStoreConnector(Record.objects.get(id=record_id))
    return rdf_delete(c, obj.query_all())

def record_post_objects(request, record_id, obj,  **kwargs):
    c = RecordStoreConnector(Record.objects.get(id=record_id))
    path = smart_path(request.path)

    g = parse_rdf(request.raw_post_data)
    var_bindings = obj.path_var_bindings(path)

    if "record_id" in var_bindings:
        assert var_bindings['record_id'] == record_id, "Mismatched: %s vs. %s"%(record_id, var_bindings['record_id'])
    else:
        var_bindings['record_id'] = record_id

    new_uris = obj.prepare_graph(g, c, var_bindings)

    return rdf_post(c, g)    

def record_put_object(request, record_id, obj, **kwargs):
    # An idempotent PUT requires:  
    #  1.  Ensure we're only putting *one* object
    #  2.  Add its external_id as an attribute in the RDF graph
    #  3.  Add any parent-child links if needed
    #  4.  Delete the thing from existing store, if it's present
    #  5.  POST the (new) thing to the store
    pass
