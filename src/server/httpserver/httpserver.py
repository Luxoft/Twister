#!/usr/bin/python

'''
This file contains the HTTP server that generates reports and runs the Java applet.
'''

import os
import sys
import re
import datetime
import socket
import json
import binascii
import MySQLdb
import cherrypy
from mako.template import Template

#

class Root:

    # Home link 1
    @cherrypy.expose
    def index(self):
        global glob_links
        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/base.htm')
        return output.render(title='Home', links=glob_links)

    # Home link 2
    @cherrypy.expose
    def home(self):
        return self.index()

    # Help link
    @cherrypy.expose
    def help(self):
        global glob_links
        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/help.htm')
        return output.render(title='Help', links=glob_links)


    # Reporting link
    @cherrypy.expose
    def rep(self, report, **args):
        global glob_fields, glob_reports, glob_links, conn, curs

        if report in glob_redirects:
            redirect_dict = glob_redirects[report]
            raise cherrypy.HTTPRedirect(redirect_dict['path'])

        if report not in glob_reports:
            output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
            return output.render(title='Missing report', links=glob_links, msg='Report <b>{0}</b> is not defined!'.format(report))

        # All info about the report, from DB XML
        report_dict = glob_reports[report]

        query = report_dict['sqlquery']

        # All variables that must be replaced in Query
        vars_to_replace = re.findall('(@.+?@)', query)


        # ------------------------------------------------------------------------------------------
        # If the user didn't select fields YET :
        # ------------------------------------------------------------------------------------------

        if vars_to_replace and not cherrypy.request.params:
            # Options are defined as: Type, Label, Data
            u_options = {}

            for opt in vars_to_replace:
                u_field = glob_fields.get(opt.replace('@', ''))
                this_option = {}

                if not u_field:
                    output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                    return output.render(links=glob_links, title=report,
                        msg='Cannot build query!<br><br>Field <b>{0}</b> is not defined in the fields section!'.format(opt.replace('@', '')))

                this_option['type'] = u_field.get('type')
                this_option['label'] = u_field.get('label')

                # Field type : User Select
                if this_option['type'] == 'UserSelect':

                    u_query = u_field.get('sqlquery')

                    if not u_query:
                        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                        return output.render(links=glob_links, title=report,
                            msg='Cannot build query!<br><br>Field <b>{0}</b> doesn\'t have a query!'.format(opt.replace('@', '')))

                    # Execute User Query
                    try:
                        curs.execute(u_query)
                    except MySQLdb.Error, e:
                        try:
                            connect_db()
                        except:
                            output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                            return output.render(links=glob_links, title=report,
                                msg='Error in query `{0}`!<br><br><b>MySQL Error {1}</b>: {2}!'.format(u_query, e.args[0], e.args[1]))

                    u_vals = curs.fetchall()

                    # No data available
                    if not u_vals:
                        this_option['data'] = []
                    # Data has one column
                    elif len(u_vals[0]) == 1:
                        field_data = [ (val[0], val[0]) for val in u_vals ]
                        this_option['data'] = field_data
                    # Data has 2 or more columns
                    else:
                        field_data = [ ( str(val[0]), str(val[0])+': '+'| '.join(val[1:]) ) for val in u_vals ]
                        this_option['data'] = field_data

                # Field type : User Text
                elif this_option['type'] == 'UserText':
                    this_option['data'] = ''

                else:
                    output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                    return output.render(title=report, links=glob_links,
                        msg='Field <b>{0}</b> is of unknown type: <b>{1}</b>!'.format(opt.replace('@', ''), this_option['type']))

                u_options[opt] = this_option

            output = Template(filename=TWISTER_PATH + '/server/httpserver/template/base.htm')
            return output.render(title=report, links=glob_links, options=u_options)


        # ------------------------------------------------------------------------------------------
        # If the user has selected the fields :
        # ------------------------------------------------------------------------------------------

        ajax_links = []

        for field in vars_to_replace:
            # The value chosen by the user
            u_select = cherrypy.request.params.get(field)
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
            try:
                connect_db()
            except:
                output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                return output.render(title=report, links=glob_links,
                    msg='Error in query `{0}`!<br><br><b>MySQL Error {1}</b>: {2}!'.format(query, e.args[0], e.args[1]))

        descr = [desc[0] for desc in curs.description]

        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/base.htm')
        return output.render(title=report, links=glob_links, ajax_link=ajax_link, user_choices=user_choices,
            report=descr, chart=report_dict['type'])


    # JSON link
    @cherrypy.expose
    def json(self, report, **args):
        global glob_reports, conn, curs

        cherrypy.response.headers['Content-Type'] = 'application/json; charset=utf-8'

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
            u_select = cherrypy.request.params.get(field)
            # Replace @variables@ with user chosen value
            query = query.replace(field, str(u_select))

        try:
            curs.execute(query)
        except MySQLdb.Error, e:
            try:
                connect_db()
            except:
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
                u_select = cherrypy.request.params.get(field)
                # Replace @variables@ with user chosen value
                query_total = query_total.replace(field, str(u_select))

            try:
                curs.execute(query_total)
            except MySQLdb.Error, e:
                try:
                    connect_db()
                except:
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
            del rows

        if (not calc_rows) or (not calc_rows[0:1]):
            output = {'aaData':[], 'error':'The select is empty!'}
            return json.dumps(output, indent=2)

        if isinstance(calc_rows[0][0], datetime.datetime):
            isDate = True
        else:
            isDate = False

        dthandler = lambda obj: obj.strftime('%Y-%m-%d %H:%M:%S') if isinstance(obj, datetime.datetime) else None
        return json.dumps({'headers':headers, 'type':report_dict['type'], 'isDate':isDate, 'aaData':calc_rows},
            indent=2, default=dthandler)


    # Error page
    @cherrypy.expose
    def default(self, code):
        global glob_links
        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
        return output.render(title='Error 404', links=glob_links, msg='Sorry, this page does not exist!')

#

def connect_db():
    global conn, curs
    conn = MySQLdb.connect(host=db_config.get('server'), db=db_config.get('database'),
                           user=db_config.get('user'), passwd=db_config.get('password'))
    curs = conn.cursor()

#

if __name__ == '__main__':

    TWISTER_PATH = os.getenv('TWISTER_PATH')
    if not TWISTER_PATH:
        print('TWISTER_PATH environment variable is not set! Exiting!')
        exit(1)
    sys.path.append(TWISTER_PATH)

    from common.xmlparser import *
    from trd_party.BeautifulSoup import BeautifulStoneSoup

    # Read XML configuration file
    FMW_PATH = TWISTER_PATH + '/config/fwmconfig.xml'
    if not os.path.exists(FMW_PATH):
        logCritical("HTTP Server: Invalid path for config file: `%s` !" % FMW_PATH)
        exit(1)
    else:
        soup = BeautifulStoneSoup(open(FMW_PATH))

    DB_CFG = soup.dbconfigfile.text
    if DB_CFG.startswith('~'):
        DB_CFG = os.getenv('HOME') + DB_CFG[1:]

    # Read DB Config File
    dbparser =  DBParser(DB_CFG)
    db_config = dbparser.db_config
    glob_fields = dbparser.getReportFields()
    glob_reports = dbparser.getReports()
    glob_redirects = dbparser.getRedirects()
    glob_links = ['Home'] + glob_reports.keys() + glob_redirects.keys() + ['Help']

    conn = None
    curs = None
    connect_db()

    # Find server IP
    serverIP = socket.gethostbyname(socket.gethostname())
    # Find server PORT
    serverPort = int(soup.httpserverport.text)
    del soup

    root = Root()

    cherrypy.config.update({'server.socket_host': '11.126.32.20', 'server.socket_port': serverPort})

    conf = {'/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': TWISTER_PATH + '/server/httpserver/static',
                },
            '/jar': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': TWISTER_PATH + '/client/userinterface/ui',
                },
            }

    cherrypy.quickstart(root, '/', config=conf)
