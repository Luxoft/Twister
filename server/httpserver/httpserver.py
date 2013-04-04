#!/usr/bin/python

# version: 2.001

# File: httpserver.py ; This file is part of Twister.

# Copyright (C) 2012 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Andrei Toma <atoma@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
This file contains the HTTP server that generates reports and runs the Java applet.
'''

import os
import sys
import re
import datetime
import json
import MySQLdb
import cherrypy
from mako.template import Template

#

class Root:

    # Java User Interface 1
    @cherrypy.expose
    def gui(self):
        output = open(TWISTER_PATH + '/server/httpserver/template/ui.htm', 'r')
        return output.read()

    # Java User Interface 2
    @cherrypy.expose
    def java(self):
        return self.gui()

    # Report link 1
    @cherrypy.expose
    def index(self, usr=''):
        if not usr: return '<br><b>Error! This link should be accessed by passing a username, eg: /index/some_user<b/>'
        if not os.path.exists('/home/%s/twister/config' % usr): return '<br><b>Error! '\
                              'Username `%s` doesn\'t have a Twister config folder!</b>' % usr

        load_config(usr) # Re-load all Database XML
        global glob_links
        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/base.htm')
        return output.render(title='Home', usr=usr, links=glob_links[usr])

    # Report link 2
    @cherrypy.expose
    def home(self, usr=''):
        return self.index(usr=usr)

    # Report link 3
    @cherrypy.expose
    def report(self, usr=''):
        return self.index(usr=usr)

    # Report link 4
    @cherrypy.expose
    def reporting(self, usr=''):
        return self.index(usr=usr)

    # Help link
    @cherrypy.expose
    def help(self, usr=''):
        if not usr: return '<br><b>Error! This link should be accessed by passing a username, eg: /help/some_user<b/>'
        if not os.path.exists('/home/%s/twister/config' % usr): return '<br><b>Error! '\
                              'Username `%s` doesn\'t have a Twister config folder!</b>' % usr

        load_config(usr) # Re-load all Database XML
        global glob_links
        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/help.htm')
        return output.render(title='Help', usr=usr, links=glob_links[usr])


    # Reporting link
    @cherrypy.expose
    def rep(self, report=None, usr=None, **args):

        if not usr: return '<br><b>Error! This link should be accessed by passing a username, eg: /rep/some_user<b/>'
        if not os.path.exists('/home/%s/twister/config' % usr): return '<br><b>Error! '\
                              'Username `%s` doesn\'t have a Twister config folder!</b>' % usr

        load_config(usr) # Re-load all Database XML
        global conn, curs
        if usr not in conn: connect_db(usr)
        global glob_fields, glob_reports, glob_links

        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0

        if not report:
            raise cherrypy.HTTPRedirect('/error')

        if report in glob_redirects[usr]:
            redirect_dict = glob_redirects[usr][report]['path']
            raise cherrypy.HTTPRedirect(redirect_dict)

        if report not in glob_reports[usr]:
            output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
            return output.render(title='Missing report', usr=usr, links=glob_links[usr], msg='Report <b>{0}</b> is not defined!'.format(report))

        # All info about the report, from DB XML
        report_dict = glob_reports[usr][report]

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
                u_field = glob_fields[usr].get(opt.replace('@', ''))
                this_option = {}

                if not u_field:
                    output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                    return output.render(links=glob_links[usr], title=report, usr=usr,
                        msg='Cannot build query!<br><br>Field <b>{0}</b> is not defined in the fields section!'.format(opt.replace('@', '')))

                this_option['type'] = u_field.get('type')
                this_option['label'] = u_field.get('label')

                # Field type : User Select
                if this_option['type'] == 'UserSelect':

                    u_query = u_field.get('sqlquery')

                    if not u_query:
                        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                        return output.render(links=glob_links[usr], title=report, usr=usr,
                            msg='Cannot build query!<br><br>Field <b>{0}</b> doesn\'t have a query!'.format(opt.replace('@', '')))

                    # Execute User Query
                    try:
                        curs[usr].execute(u_query)
                    except MySQLdb.Error, e:
                        try:
                            connect_db(usr)
                        except:
                            pass

                        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                        return output.render(links=glob_links[usr], title=report, usr=usr,
                            msg='Error in query `{0}`!<br><br><b>MySQL Error {1}</b>: {2}!'.format(u_query, e.args[0], e.args[1]))

                    try:
                        u_vals = curs[usr].fetchall()
                    except Exception, e:
                        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                        return output.render(links=glob_links[usr], title=report, usr=usr,
                            msg='Error in query `{0}`!<br><br><b>Exception</b>: {1}!'.format(u_query, e))

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
                    return output.render(title=report, links=glob_links[usr], usr=usr,
                        msg='Field <b>{0}</b> is of unknown type: <b>{1}</b>!'.format(opt.replace('@', ''), this_option['type']))

                u_options[opt] = this_option

            output = Template(filename=TWISTER_PATH + '/server/httpserver/template/base.htm')
            return output.render(title=report, usr=usr, links=glob_links[usr], options=u_options)


        # ------------------------------------------------------------------------------------------
        # If the user has selected the fields :
        # ------------------------------------------------------------------------------------------

        ajax_links = []

        # ... For normal Queries ...
        for field in vars_to_replace:
            # The value chosen by the user
            u_select = cherrypy.request.params.get(field)
            if not u_select: u_select = ''
            ajax_links.append(field +'='+ u_select)
            # Replace @variables@ with user chosen value
            query = query.replace(field, str(u_select))

        ajax_links = sorted( list(set(ajax_links)) )
        ajax_link = '/json/' + report + '/' + usr + '?' + '&'.join(ajax_links)
        user_choices = ('", '.join(ajax_links))
        user_choices = user_choices.replace('@', '').replace('=', '="')+'"'
        del ajax_links

        try:
            curs[usr].execute(query)
        except MySQLdb.Error, e:
            try:
                connect_db(usr)
            except:
                pass
            #
            output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
            return output.render(title=report, links=glob_links[usr], usr=usr,
                msg='Error in query `{0}`!<br><br><b>MySQL Error {1}</b>: {2}!'.format(query, e.args[0], e.args[1]))

        descr = [desc[0] for desc in curs[usr].description]

        # Write DEBUG
        #DEBUG.write(report +' -> '+ user_choices +' -> '+ query + '\n\n') ; DEBUG.flush()


        # ... For Query Compare side by side, the table is double ...
        query_compr = report_dict['sqlcompr']

        if query_compr:
            # All variables that must be replaced in Query
            vars_to_replace = re.findall('(@.+?@)', query_compr)

            for field in vars_to_replace:
                # The value chosen by the user
                u_select = cherrypy.request.params.get(field)
                # Replace @variables@ with user chosen value
                query_compr = query_compr.replace(field, str(u_select))

            try:
                curs[usr].execute(query_compr)
            except MySQLdb.Error, e:
                try:
                    connect_db(usr)
                except:
                    pass
                #
                output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
                return output.render(title=report, links=glob_links[usr], usr=usr,
                msg='Error in query `{0}`!<br><br><b>MySQL Error {1}</b>: {2}!'.format(query_compr, e.args[0], e.args[1]))

            headers_tot = [desc[0] for desc in curs[usr].description]

            # Update headers: must contain both headers.
            descr = descr + ['vs.'] + headers_tot

            # Write DEBUG
            #DEBUG.write(report +' -> '+ user_choices +' -> '+ query_compr + '\n\n') ; DEBUG.flush()

        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/base.htm')
        return output.render(usr=usr, title=report, links=glob_links[usr], ajax_link=ajax_link, user_choices=user_choices,
            report=descr, chart=report_dict['type'])


    # JSON link
    @cherrypy.expose
    def json(self, report, usr, **args):

        if not usr:
            output = {'aaData':[], 'error':'Error! This link should be accessed by passing a username, eg: /json/some_report/some_user'}
            return json.dumps(output, indent=2)

        if not os.path.exists('/home/%s/twister/config' % usr):
            output = {'aaData':[], 'error':'Error! Username `%s` doesn\'t have a Twister config folder!' % usr}
            return json.dumps(output, indent=2)

        load_config(usr) # Re-load all Database XML
        global conn, curs
        if usr not in conn: connect_db(usr)
        global glob_reports

        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0

        if report not in glob_reports[usr]:
            output = {'aaData':[], 'error':'Report `{0}` is not in the list of defined reports!'.format(report)}
            return json.dumps(output, indent=2)

        # All info about the report, from DB XML.
        report_dict = glob_reports[usr][report]
        query = report_dict['sqlquery']

        # All variables that must be replaced in Query
        vars_to_replace = re.findall('(@.+?@)', query)

        for field in vars_to_replace:
            # The value chosen by the user
            u_select = cherrypy.request.params.get(field)
            # Replace @variables@ with user chosen value
            query = query.replace(field, str(u_select))

        try:
            curs[usr].execute(query)
        except MySQLdb.Error, e:
            try:
                connect_db(usr)
            except:
                pass

            output = {'aaData':[], 'error':'Error in query `{0}`! MySQL Error {1}: {2}!'.format(query, e.args[0], e.args[1])}
            return json.dumps(output, indent=2)

        headers = [desc[0] for desc in curs[usr].description]
        rows = curs[usr].fetchall()
        del query

        query_total = report_dict['sqltotal']
        query_compr = report_dict['sqlcompr']


        # ... Calculate SQL Query Total ...
        if query_total:
            # All variables that must be replaced in Query
            vars_to_replace = re.findall('(@.+?@)', query_total)

            for field in vars_to_replace:
                # The value chosen by the user
                u_select = cherrypy.request.params.get(field)
                # Replace @variables@ with user chosen value
                query_total = query_total.replace(field, str(u_select))

            try:
                curs[usr].execute(query_total)
            except MySQLdb.Error, e:
                try:
                    connect_db(usr)
                except:
                    pass
                #
                output = {'aaData':[], 'error':'Error in query total `{0}`! MySQL Error {1}: {2}!'.format(query_total, e.args[0], e.args[1])}
                return json.dumps(output, indent=2)

            headers_tot = [desc[0] for desc in curs[usr].description]
            rows_tot = curs[usr].fetchall()

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
                tot_row = list(rows_tot[i])

                # Null and None values must be numbers
                if not row[0]: row = (0.0, row[1])
                if not row[1]: row = (row[0], 0.0)
                if not tot_row[0]: tot_row[0] = 0.0
                if not tot_row[1]: tot_row[1] = 0.1

                # Calculate percent...
                percent = '%.2f' % ( float(row[1]) / tot_row[1] * 100.0 )
                # Using the header from Total, because it might be Null in the first query
                calc_rows.append([tot_row[0], float(percent)])


        # ... SQL Query Compare side by side ...
        elif query_compr:
            # All variables that must be replaced in Query
            vars_to_replace = re.findall('(@.+?@)', query_compr)

            for field in vars_to_replace:
                # The value chosen by the user
                u_select = cherrypy.request.params.get(field)
                # Replace @variables@ with user chosen value
                query_compr = query_compr.replace(field, str(u_select))

            try:
                curs[usr].execute(query_compr)
            except MySQLdb.Error, e:
                try:
                    connect_db(usr)
                except:
                    pass
                #
                output = {'aaData':[], 'error':'Error in query compare `{0}`! MySQL Error {1}: {2}!'.format(query_total, e.args[0], e.args[1])}
                return json.dumps(output, indent=2)

            headers_tot = [desc[0] for desc in curs[usr].description]
            rows_tot = curs[usr].fetchall()

            if len(headers) != len(headers_tot): # Must be the same number of columns
                output = {'aaData':[], 'error':'The first query has {0} columns and the second has {1} columns!'.format(len(headers), len(headers_tot))}
                return json.dumps(output, indent=2)

            headers_len = len(headers)
            rows_max_size = max(len(rows), len(rows_tot))
            calc_rows = []

            for i in range(rows_max_size):
                r1 = rows[i:i+1]
                r2 = rows_tot[i:i+1]
                if not r1: r1 = [' ' for i in range(headers_len)]
                else: r1 = r1[0]
                if not r2: r2 = [' ' for i in range(headers_len)]
                else: r2 = r2[0]
                calc_rows.append( tuple(r1) +(' <---> ',)+ tuple(r2) )

            # Update headers: must contain both headers.
            headers = headers + ['vs.'] + headers_tot

        # ... Normal Query ...
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
    def error(self):
        global glob_links
        output = Template(filename=TWISTER_PATH + '/server/httpserver/template/error.htm')
        return output.render(title='Error 404', links=[], msg='Sorry, this page does not exist!')

#

def load_config(usr):
    '''
    Read DB Config File
    '''
    global dbparser, db_config
    global glob_fields, glob_reports, glob_redirects, glob_links

    if not os.path.exists('/home/%s/twister' % usr):
        print("HTTP Server: Cannot find Twister for usr `%s` !" % usr)
        return False

    # Read usr XML config file...
    FMW_PATH = '/home/%s/twister/config/fwmconfig.xml' % usr
    if not os.path.exists(FMW_PATH):
        print("HTTP Server: Invalid path for config file: `%s` !" % FMW_PATH)
        return False

    s = open(FMW_PATH).read()
    a = s.find('<DbConfigFile>') + len('<DbConfigFile>')
    b = s.find('</DbConfigFile>')

    # Databse config path file...
    DBCFG_PATH = s[a:b]
    if DBCFG_PATH.startswith('~'):
        DBCFG_PATH = os.getenv('HOME') + DBCFG_PATH[1:]
    del s

    # Create database parser...
    if usr not in dbparser:
        print('Parsing the Config for usr `%s`, the first time...\n' % usr)
        dbparser[usr] =  DBParser(DBCFG_PATH)
        db_config[usr] = dbparser[usr].db_config

    glob_fields[usr] = dbparser[usr].getReportFields()
    glob_reports[usr] = dbparser[usr].getReports()
    glob_redirects[usr] = dbparser[usr].getRedirects()
    glob_links[usr] = ['Home'] + glob_reports[usr].keys() + glob_redirects[usr].keys() + ['Help']

#

def connect_db(usr):
    global conn, curs
    if usr not in conn:
        print('Connecting to the Database for the first time...\n')

    conn[usr] = MySQLdb.connect(host=db_config[usr].get('server'), db=db_config[usr].get('database'),
                           user=db_config[usr].get('user'),    passwd=db_config[usr].get('password'))
    curs[usr] = conn[usr].cursor()

#

if __name__ == '__main__':

    TWISTER_PATH = os.getenv('TWISTER_PATH')
    if not TWISTER_PATH:
        print('TWISTER_PATH environment variable is not set! Exiting!')
        exit(1)

    serverPort = sys.argv[1:2]
    if not serverPort:
        print('HTTP Server must start with parameter PORT number!')
        exit(1)

    sys.path.append(TWISTER_PATH)
    from common.xmlparser import DBParser

    # Reporting server IP and PORT
    serverIP = '0.0.0.0'
    serverPort = int(serverPort[0])

    dbparser =  {}
    db_config = {}
    glob_fields  = {}
    glob_reports = {}
    glob_redirects = {}
    glob_links   = {}
    conn = {}
    curs = {}

    # DEBUG file
    #DEBUG = open(TWISTER_PATH + '/config/reporting.query', 'w')

    root = Root()

    cherrypy.config.update({'server.socket_host': serverIP, 'server.socket_port': serverPort})

    conf = {
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': TWISTER_PATH + '/server/httpserver/static',
                },
            '/gui': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': TWISTER_PATH + '/server/httpserver/gui',
                },
            }

    cherrypy.quickstart(root, '/', config=conf)
