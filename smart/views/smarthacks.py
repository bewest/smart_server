"""
Quick hacks for SMArt

Ben Adida
"""

from base import *
from smart.lib import utils
from django.http import HttpResponseBadRequest
from django.conf import settings
import psycopg2
import psycopg2.extras
from rdflib import ConjunctiveGraph, Namespace, Literal
from StringIO import StringIO
import smart.models



SAMPLE_NOTIFICATION = {
    'id' : 'foonotification',
    'sender' : {'email':'foo@smart.org'},
    'created_at' : '2010-06-21 13:45',
    'content' : 'a sample notification',
    }

@paramloader()
def record_list(request, account):
    return render_template('record_list', {'records': [ar.record for ar in account.accountrecord_set.all()]}, type='xml')

@paramloader()
def account_notifications(request, account):
    return render_template('notifications', {'notifications': [SAMPLE_NOTIFICATION]})

def record_by_token(request):
    print "token", request.oauth_request.token
    t = request.oauth_request.token
    return render_template('record', {'record': t.share.record})

@paramloader()
def record_info(request, record):
    return render_template('record', {'record': record})
@paramloader()
def record_apps(request, record):
    return render_template('phas', {'phas': [ra.app for ra in record.recordapp_set.all()]})


@paramloader()
def record_add_app(request, record, app):
    """
    expecting
    PUT /records/{record_id}/apps/{app_email}
    """
    try:
        RecordApp.objects.create(record = record, app = app)
    except:
        # we assume htis is a duplicate, no problem
        pass

    return DONE

@paramloader()
def record_remove_app(request, record, app):
    """
    expecting
    DELETE /records/{record_id}/apps/{app_email}
    """
    RecordApp.objects.get(record = record, app = app).delete()
    return DONE

#@paramloader()
#
#def meds(request, medcall, record):
#    return utils.get_rdf_meds()
#    fixture = "meds_%s.ccr"%("")
#    raw_xml = render_template_raw("fixtures/%s"%fixture, {})
#    rdf_xml = utils.meds_as_rdf(raw_xml)
#    print "rdf version ", rdf_xml
#    return HttpResponse(rdf_xml, mimetype="application/rdf+xml")
