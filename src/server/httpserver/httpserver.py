
import os
import sys
import re
import datetime
import socket
import json
import binascii
import MySQLdb

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('TWISTER_PATH environment variable is not set! Exiting!')
    exit(1)
sys.path.insert(0, TWISTER_PATH)

from common.xmlparser import *
from trd_party.bottle import *
from trd_party import bottle

#
dbparser = DBParser(TWISTER_PATH + os.sep + 'config/db.xml')
db_config = dbparser.db_config
glob_fields = dbparser.getReportFields()
glob_reports = dbparser.getReports()
glob_redirects = dbparser.getRedirects()
glob_links = ['Home'] + glob_reports.keys() + glob_redirects.keys() + ['Help']
#
conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
        user=db_config.get('user'), passwd=db_config.get('password'))
curs = conn.cursor()
#

# --------------------------------------------------------------------------------------------------
#           I N D E X
# --------------------------------------------------------------------------------------------------

@route('/')
@route('/index')
@route('/index/')
@route('/home')
@route('/home/')
def index():
    global glob_links
    output = template(os.getcwd()+'/template/base.htm', title='Home', links=glob_links)
    return output


# --------------------------------------------------------------------------------------------------
#           R E P O R T S
# --------------------------------------------------------------------------------------------------

@get('/rep/<report>')
@get('/rep/<report>/')
def reports(report):
    global glob_fields, glob_reports, glob_links

    if report in glob_redirects:
        redirect_dict = glob_redirects[report]
        redirect(redirect_dict['path'])

    if report not in glob_reports:
        output = template(os.getcwd()+'/template/error.htm', links=glob_links, title='Missing report',
            msg='Report <b>{0}</b> is not defined!'.format(report))
        return output

    # All info about the report, from DB XML
    report_dict = glob_reports[report]

    query = report_dict['sqlquery']

    # All variables that must be replaced in Query
    vars_to_replace = re.findall('(@.+?@)', query)


    # ----------------------------------------------------------------------------------------------
    # If the user didn't select fields YET :
    # ----------------------------------------------------------------------------------------------

    if vars_to_replace and not request.GET.keys():
        # Options are defined as: Type, Label, Data
        u_options = {}

        for opt in vars_to_replace:
            u_field = glob_fields.get(opt.replace('@', ''))
            this_option = {}

            if not u_field:
                output = template(os.getcwd()+'/template/error.htm', links=glob_links, title=report,
                    msg='Cannot build query!<br><br>Field <b>{0}</b> is not defined in the fields section!'.format(opt.replace('@', '')))
                return output

            this_option['type'] = u_field.get('type')
            this_option['label'] = u_field.get('label')

            # Field type : User Select
            if this_option['type'] == 'UserSelect':

                u_query = u_field.get('sqlquery')

                if not u_query:
                    output = template(os.getcwd()+'/template/error.htm', links=glob_links, title=report,
                        msg='Cannot build query!<br><br>Field <b>{0}</b> doesn\'t have a query!'.format(opt.replace('@', '')))
                    return output

                # Execute User Query
                try:
                    curs.execute(u_query)
                except MySQLdb.Error, e:
                    output = template(os.getcwd()+'/template/error.htm', links=glob_links, title=report,
                        msg='Error in query `{0}`!<br><br><b>MySQL Error {1}</b>: {2}!'.format(u_query, e.args[0], e.args[1]))
                    return output

                u_vals = curs.fetchall()

                if not u_vals:
                    this_option['data'] = []
                elif len(u_vals[0]) == 1:
                    field_data = [ (val[0], val[0]) for val in u_vals ]
                    this_option['data'] = field_data
                else:
                    field_data = [ (val[0], str(val[0])+': '+'| '.join(val[1:])) for val in u_vals ]
                    this_option['data'] = field_data

            # Field type : User Text
            elif this_option['type'] == 'UserText':
                this_option['data'] = ''

            else:
                output = template(os.getcwd()+'/template/error.htm', links=glob_links, title=report,
                    msg='Field <b>{0}</b> is of unknown type: <b>{1}</b>!'.format(opt.replace('@', ''), this_option['type']))
                return output

            u_options[opt] = this_option

        output = template(os.getcwd()+'/template/base.htm', title=report, links=glob_links, options=u_options)
        return output


    # ----------------------------------------------------------------------------------------------
    # If the user has selected the fields :
    # ----------------------------------------------------------------------------------------------

    ajax_links = []

    for field in vars_to_replace:
        # The value chosen by the user
        u_select = request.GET.get(field)
        ajax_links.append(field +'='+ u_select)
        # Replace @variables@ with user chosen value
        query = query.replace(field, str(u_select))

    ajax_link = '/json/' + report + '?' + '&'.join(ajax_links)
    user_choices = ('", '.join(ajax_links))
    user_choices = user_choices.replace('@', '').replace('=', '="')+'"'
    del ajax_links

    try:
        curs.execute(query)
    except MySQLdb.Error, e:
        output = template(os.getcwd()+'/template/error.htm', links=glob_links, title=report,
            msg='Error in query `{0}`!<br><br><b>MySQL Error {1}</b>: {2}!'.format(query, e.args[0], e.args[1]))
        return output

    descr = [desc[0] for desc in curs.description]

    output = template(os.getcwd()+'/template/base.htm', title=report, links=glob_links, ajax_link=ajax_link, user_choices=user_choices,
        report=descr, chart=report_dict['type'])
    return output

#

@get('/json/<report>')
@get('/json/<report>/')
def xhr_report(report):

    global glob_reports
    response.content_type = 'application/json'

    if report not in glob_reports:
        output = {'aaData':[], 'error':'Report `{0}` is not in the list of defined reports!'.format(report)}
        return json.dumps(output, indent=2)

    # All info about the report, from DB XML.
    report_dict = glob_reports[report]
    query = report_dict['sqlquery']

    # All variables that must be replaced in Query
    vars_to_replace = re.findall('(@.+?@)', query)

    for field in vars_to_replace:
        # The value chosen by the user
        u_select = request.GET.get(field)
        # Replace @variables@ with user chosen value
        query = query.replace(field, str(u_select))

    try:
        curs.execute(query)
    except MySQLdb.Error, e:
        output = {'aaData':[], 'error':'Error in query `{0}`! MySQL Error {1}: {2}!'.format(query, e.args[0], e.args[1])}
        return json.dumps(output, indent=2)

    headers = [desc[0] for desc in curs.description]
    rows = curs.fetchall()
    del query

    query_total = report_dict['sqltotal']

    if query_total:
        # All variables that must be replaced in Query
        vars_to_replace = re.findall('(@.+?@)', query_total)

        for field in vars_to_replace:
            # The value chosen by the user
            u_select = request.GET.get(field)
            # Replace @variables@ with user chosen value
            query_total = query_total.replace(field, str(u_select))

        try:
            curs.execute(query_total)
        except MySQLdb.Error, e:
            output = {'aaData':[], 'error':'Error in query `{0}`! MySQL Error {1}: {2}!'.format(query_total, e.args[0], e.args[1])}
            return json.dumps(output, indent=2)

        headers_tot = [desc[0] for desc in curs.description]
        rows_tot = curs.fetchall()

        if len(headers) != len(headers_tot):
            output = {'aaData':[], 'error':'The first query has {0} columns and the second has {1} columns!'.format(len(headers), len(headers_tot))}
            return json.dumps(output, indent=2)

        if len(rows) != len(rows_tot):
            output = {'aaData':[], 'error':'The first query has {0} rows and the second has {1} rows!'.format(len(rows), len(rows_tot))}
            return json.dumps(output, indent=2)

        # Will calculate the new rows like this:
        # The first column of the first query will not be changed
        # The second row of the first query / the second row of the second query * 100
        calc_rows = []

        for i in range(len(rows)):
            row = rows[i]
            # "None" values must be converted to Float
            if not row[1]: row = (row[0], 0.0)
            # Calculate percent...
            percent = '%.2f' % ( float(row[1]) / rows_tot[i][1] * 100.0 )
            # Using the header from Total, because it might be Null in the first query
            calc_rows.append([rows_tot[i][0], float(percent)])

    else:
        calc_rows = rows

    if isinstance(calc_rows[0][0], datetime):
        isDate = True
    else:
        isDate = False

    dthandler = lambda obj: obj.strftime('%Y-%m-%d %H:%M:%S') if isinstance(obj, datetime) else None
    return json.dumps({'headers':headers, 'type':report_dict['type'], 'isDate':isDate, 'aaData':calc_rows},
        indent=2, default=dthandler)

# --------------------------------------------------------------------------------------------------
#           O T H E R    P A G E S
# --------------------------------------------------------------------------------------------------

@route('/help')
@route('/help/')
def help_pages():
    output = template(os.getcwd()+'/template/help.htm', title='Help', links=glob_links)
    return output

@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.getcwd())

@error(403)
def err403(code):
    output = template(os.getcwd()+'/template/error.htm', links=glob_links, title='Error 403',
        msg='The parameter you passed has the wrong format!')
    return output

@error(404)
def err404(code):
    output = template(os.getcwd()+'/template/error.htm', links=glob_links, title='Error 404',
        msg='Sorry, this page does not exist!')
    return output

#

if __name__ == '__main__':

    serverIP = socket.gethostbyname(socket.gethostname())
    bottle.debug(True)
    run(host=serverIP, port=8080, reloader=True)
