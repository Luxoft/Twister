
# File: CeReports.py ; This file is part of Twister.

# version: 3.011

# Copyright (C) 2012-2014 , Luxoft

# Authors:
#    Andrei Costachi <acostachi@luxoft.com>
#    Cristi Constantin <crconstantin@luxoft.com>
#    Daniel Cioata <dcioata@luxoft.com>
#    Mihai Tudoran <mtudoran@luxoft.com>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This file contains the Reporting Server.
It is used to view the results of the test executions.
The reports can be fully customized, by editing the DB.xml file.
The INDEX/ HOME links force the reload of the DB.xml file,
the rest of the links just use the cached data, from last reload.
"""

import os
import sys
import re
import time
import datetime
import json
import mako
import binascii

import MySQLdb
import cherrypy
from collections import OrderedDict
from mako.template import Template

TWISTER_PATH = os.getenv('TWISTER_PATH')
if not TWISTER_PATH:
    print('\n$TWISTER_PATH environment variable is not set! Exiting!\n')
    exit(1)
if TWISTER_PATH not in sys.path:
    sys.path.append(TWISTER_PATH)

from common.helpers    import *
from common.tsclogging import *
from common.xmlparser  import *

if mako.__version__ < '0.7':
    logWarning('Warning! Mako-template version `{}` is old! Some pages might crash!\n'.format(mako.__version__))



class ReportingServer(object):
    """
    Reporting server class.
    """

    db_parser = {}
    glob_fields  = {}
    glob_reports = {}
    glob_redirects = {}
    glob_links = {}
    timers = {}


    def __init__(self, project):
        """
        Initialization function.
        """
        self.project = project


    def load_config(self, usr, force=False):
        """
        Read DB Config File for 1 user.
        """
        if not os.path.isdir(userHome(usr) + '/twister/config'):
            logError('Report Server: Cannot find Twister for user `{}` !'.format(usr))
            return False

        # Get the path to DB.XML
        db_file = self.project.get_user_info(usr, 'db_config')
        if not db_file:
            logError('Report Server: Null DB.XML file for user `{}`! Nothing to do!'.format(usr))
            return False

        # Current timer
        c_time = time.time()

        # Create database parser IF necessary, or FORCED, or old connection...
        if force or (usr not in self.db_parser) or (c_time - self.timers.get(usr, 0) > 5.0):

           # logDebug('Rebuilding fields, reports and redirects for user `{}`...'.format(usr))

            self.timers[usr] = c_time
            self.db_parser[usr] = True
            self.glob_fields[usr]  = OrderedDict()
            self.glob_reports[usr] = OrderedDict()
            self.glob_redirects[usr] = OrderedDict()

            # DB.xml + Shared DB parser
            users_groups = self.project._parse_users_and_groups()
            shared_db_path = users_groups['shared_db_cfg']
            db_cfg_role = 'CHANGE_DB_CFG' in users_groups['users'][usr]['roles']

            # Use shared DB or not ?
            use_shared_db = self.project.get_user_info(usr, 'use_shared_db')
            if use_shared_db and use_shared_db.lower() in ['true', 'yes']:
                use_shared_db = True
            else:
                use_shared_db = False

            dbp = DBParser(usr, db_file, shared_db_path, use_shared_db)
            report_queries = dbp.get_reports(db_cfg_role)
            del dbp

            for host_db in report_queries:

                self.glob_fields[usr].update( report_queries[host_db]['fields'] )
                self.glob_reports[usr].update( report_queries[host_db]['reports'] )
                self.glob_redirects[usr].update( report_queries[host_db]['redirects'] )

                # There are more types of reports:
                # Normal links, like Home, Help and other normal reports
                # Redirect links, that don't contain reports
                # Folders, that don't go anywhere, are just labels for reports
                self.glob_links[usr] = [{'link': 'Home', 'type': 'link'}] + \
                       [{
                         'link': k,
                         'type': 'link',
                         'folder': v.get('folder', ''),
                         'srvr': '/'.join( v.get('srv_db', ['n', 'a'])[:2] )
                        } \
                       for k, v in self.glob_reports[usr].iteritems()] + \
                       [{'link': k, 'folder': '', 'type': 'redir'} \
                       for k in self.glob_redirects[usr] ] + \
                       [{'link': 'Help', 'folder': '', 'type': 'link'}]

        return True


    @cherrypy.expose
    def index(self, usr=''):
        """
        The index page.
        """
        logFull('CeReports:index')

        if not usr:
            users = self.project.list_users()
            output = Template(filename=TWISTER_PATH + '/server/template/rep_base.htm')
            return output.render(title='Users', usr='#' + '#'.join(users), links=[])

        if not os.path.isdir(userHome(usr) + '/twister/config'):
            return '<br><b>Error! Username `{}` doesn\'t have a Twister config folder!</b>'.format(usr)

        # FORCE re-load all Database XML on INDEX/ HOME links !
        self.load_config(usr, True)
        output = Template(filename=TWISTER_PATH + '/server/template/rep_base.htm')
        return output.render(title='Home', usr=usr, links=self.glob_links[usr])

    # Report link 2
    @cherrypy.expose
    def home(self, usr=''):
        """ Get reporting link 2 """
        return self.index(usr=usr)

    # Report link 3
    @cherrypy.expose
    def report(self, usr=''):
        """ Get reporting link 3 """
        return self.index(usr=usr)

    # Report link 4
    @cherrypy.expose
    def reporting(self, usr=''):
        """ Get reporting link 4 """
        return self.index(usr=usr)


    @cherrypy.expose
    def help(self, usr=''):
        """ Help page """
        logFull('CeReports:help')

        if not usr:
            return '<br><b>Error! This link should be accessed by passing a username, eg: /help/some_user<b/>'

        if not os.path.isdir(userHome(usr) + '/twister/config'):
            return '<br><b>Error! Username `{}` doesn\'t have a Twister config folder!</b>'.format(usr)

        self.load_config(usr) # Re-load all Database XML
        output = Template(filename=TWISTER_PATH + '/server/template/rep_help.htm')
        return output.render(title='Help', usr=usr, links=self.glob_links[usr])


    @cherrypy.expose
    def rep(self, report=None, usr=None, **args):
        """
        Reporting link.
        """
        logFull('CeReports:rep')

        if not usr:
            return '<br><b>Error! This link should be accessed by passing a username, eg: /rep/some_user<b/>'

        if not os.path.isdir(userHome(usr) + '/twister/config'):
            return '<br><b>Error! Username `{}` doesn\'t have a Twister config folder!</b>'.format(usr)

        self.load_config(usr) # Re-load all Database XML

        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0

        if not report:
            raise cherrypy.HTTPRedirect('/error')

        if report in self.glob_redirects[usr]:
            redirect_dict = self.glob_redirects[usr][report]['path']
            raise cherrypy.HTTPRedirect(redirect_dict)

        if report not in self.glob_reports[usr]:
            output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
            return output.render(title='Missing report', usr=usr,
                links=self.glob_links[usr],
                msg='Report `<b>{}</b>` is not defined!<br/><br/>'
                    'Go <a href="/report/home/{}">Home</a> ...'.format(report, usr))

        # All info about the report, from DB XML
        report_dict = self.glob_reports[usr][report]

        query = report_dict['sqlquery']
        db_pair = report_dict['srv_db']
        db_server, db_name, db_user, db_passwd = report_dict['srv_db']

        logDebug('Prepare {} report `{}`, for user `{}`...'.format(
                 'Shared' if report_dict['shared_db'] else 'User', report, usr))

        conn = self.project.dbmgr.connect_db(usr, *db_pair, shared_db=report_dict['shared_db'])
        if not conn:
            output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
            return output.render(links=self.glob_links[usr], title=report, usr=usr,
                msg='Cannot connect to MySql server `{} / {}` !'.format(db_server, db_name))

        curs = conn.cursor()

        # All variables that must be replaced in Query
        vars_to_replace = re.findall('(@.+?@)', query)

        # ------------------------------------------------------------------------------------------
        # If the user didn't select fields YET :
        # ------------------------------------------------------------------------------------------

        if vars_to_replace and not cherrypy.request.params:
            # Options are defined as: Type, Label, Data
            u_options = OrderedDict()

            for opt in vars_to_replace:
                u_field = self.glob_fields[usr].get(opt.replace('@', ''))
                this_option = {}

                if not u_field:
                    output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
                    return output.render(links=self.glob_links[usr], title=report, usr=usr,
                        msg='Cannot build query!<br><br>Field `<b>{}</b>` '\
                            'is not defined in the fields section!'.format(opt.replace('@', '')))

                this_option['type'] = u_field.get('type')
                this_option['label'] = u_field.get('label')

                # Field type : User Select
                if this_option['type'] == 'UserSelect':

                    u_query = u_field.get('sqlquery')

                    if not u_query:
                        output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
                        return output.render(links=self.glob_links[usr], title=report, usr=usr,
                            msg='Cannot build query!<br><br>Field `<b>{}</b>` doesn\'t '\
                            'have a query!'.format(opt.replace('@', '')))

                    # Execute User Query
                    try:
                        curs.execute(u_query)
                    except MySQLdb.Error as e:
                        output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
                        return output.render(links=self.glob_links[usr], title=report, usr=usr,
                            msg='Error in query `{}`!<br><br><b>MySQL Error {}</b>: {}!'.format(
                                u_query, e.args[0], e.args[1]))

                    try:
                        u_vals = curs.fetchall()
                    except Exception, e:
                        output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
                        return output.render(links=self.glob_links[usr], title=report, usr=usr,
                            msg='Error in query `{}`!<br><br><b>Exception</b>: {}!'.format(u_query, e))

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
                    output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
                    return output.render(title=report, links=self.glob_links[usr], usr=usr,
                        msg='Field `<b>{}</b>` is of unknown type: <b>{}</b>!'.format(
                            opt.replace('@', ''), this_option['type']))

                u_options[opt] = this_option

            output = Template(filename=TWISTER_PATH + '/server/template/rep_base.htm')
            return output.render(title=report, usr=usr, links=self.glob_links[usr], options=u_options)


        # ------------------------------------------------------------------------------------------
        # If the user has selected the fields :
        # ------------------------------------------------------------------------------------------

        ajax_links = []

        # ... For normal Queries ...
        for field in vars_to_replace:
            # The value chosen by the user
            u_select = cherrypy.request.params.get(field)
            if not u_select:
                u_select = ''
            ajax_links.append(field +'='+ u_select)
            # Replace @variables@ with user chosen value
            query = query.replace(field, str(u_select))

        ajax_links = sorted( list(set(ajax_links)) )
        ajax_link = '/report/json/' + report + '/' + usr + '?' + '&'.join(ajax_links)
        user_choices = ('", '.join(ajax_links))
        user_choices = user_choices.replace('@', '').replace('=', '="')+'"'
        del ajax_links

        try:
            curs.execute(query)
        except MySQLdb.Error as e:
            output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
            return output.render(title=report, links=self.glob_links[usr], usr=usr,
                msg='Error in query `{}`!<br><br><b>MySQL Error {}</b>: {}!'.format(query, e.args[0], e.args[1]))

        descr = [desc[0] for desc in curs.description]

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
                curs.execute(query_compr)
            except MySQLdb.Error as e:
                output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
                return output.render(title=report, links=self.glob_links[usr], usr=usr,
                    msg='Error in query `{}`!<br><br><b>MySQL Error {}</b>: {}!'.format(query_compr, e.args[0], e.args[1]))

            headers_tot = [desc[0] for desc in curs.description]

            # Update headers: must contain both headers.
            descr = descr + ['vs.'] + headers_tot

            # Write DEBUG
            #DEBUG.write(report +' -> '+ user_choices +' -> '+ query_compr + '\n\n') ; DEBUG.flush()

        output = Template(filename=TWISTER_PATH + '/server/template/rep_base.htm')
        return output.render(usr=usr, title=report, links=self.glob_links[usr],
                             ajax_link=ajax_link, user_choices=user_choices,
                             report=descr, chart=report_dict['type'])


    @cherrypy.expose
    def json(self, report, usr, **args):
        """
        The report data, in json format.
        """
        logFull('CeReports:json')

        if not usr:
            output = {'aaData':[], 'error':'Error! This link should be '\
                      'accessed by passing a username, eg: ' \
                      '/json/some_report/some_user'}
            return json.dumps(output, indent=2)

        if not os.path.isdir(userHome(usr) + '/twister/config'):
            output = {'aaData':[], 'error':'Error! Username `{}` doesn\'t have '\
                'a Twister config folder!'.format(usr)}
            return json.dumps(output, indent=2)

        self.load_config(usr) # Re-load all Database XML

        cherrypy.response.headers['Content-Type']  = 'application/json; charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        cherrypy.response.headers['Pragma']  = 'no-cache'
        cherrypy.response.headers['Expires'] = 0

        if report not in self.glob_reports[usr]:
            output = {'aaData':[], 'error':'Report `{}` is not in the list of defined reports!'.format(report)}
            return json.dumps(output, indent=2)

        # All info about the report, from DB XML.
        report_dict = self.glob_reports[usr][report]

        query = report_dict['sqlquery']
        db_pair = report_dict['srv_db']
        db_server, db_name, db_user, db_passwd = report_dict['srv_db']

        conn = self.project.dbmgr.connect_db(usr, *db_pair, shared_db=report_dict['shared_db'])
        if not conn:
            output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
            return output.render(links=self.glob_links[usr], title=report, usr=usr,
                msg='Cannot connect to MySql server `{} / {}` !'.format(db_server, db_name))

        curs = conn.cursor()

        # All variables that must be replaced in Query
        vars_to_replace = re.findall('(@.+?@)', query)

        for field in vars_to_replace:
            # The value chosen by the user
            u_select = cherrypy.request.params.get(field)
            # Replace @variables@ with user chosen value
            query = query.replace(field, str(u_select))

        try:
            curs.execute(query)
        except MySQLdb.Error as e:
            output = {'aaData':[], 'error':'Error in query `{}`! MySQL Error {}: {}!'.format(query, e.args[0], e.args[1])}
            return json.dumps(output, indent=2)

        headers = [desc[0] for desc in curs.description]
        rows = curs.fetchall()
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
                curs.execute(query_total)
            except MySQLdb.Error as e:
                output = {'aaData':[], 'error':'Error in query total `{}`! MySQL Error {}: {}!'.format(query_total, e.args[0], e.args[1])}
                return json.dumps(output, indent=2)

            headers_tot = [desc[0] for desc in curs.description]
            rows_tot = curs.fetchall()

            if len(headers) != len(headers_tot):
                output = {'aaData':[], 'error':'The first query has {} columns and the second has {} columns!'
                    .format(len(headers), len(headers_tot))}
                return json.dumps(output, indent=2)

            # Will calculate the new rows like this:
            # The first column of the first query will not be changed
            # The second row of the first query / the second row of the second query * 100
            calc_rows = []

            rows = {r[0]:r[1] for r in rows}
            rows_tot = {r[0]:r[1] for r in rows_tot}

            for rnb in rows_tot.keys():
                if rnb in rows.keys():
                    # Calculate percent...
                    percent = '%.2f' % ( float(rows[rnb]) / rows_tot[rnb] * 100.0 )
                    # Using the header from Total, because it might be Null in the first query
                    calc_rows.append([rnb, float(percent)])
                else:
                    calc_rows.append([rnb, 0.0])

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
                curs.execute(query_compr)
            except MySQLdb.Error as e:
                output = {'aaData':[], 'error':'Error in query compare `{}`! '\
                    'MySQL Error {}: {}!'.format(query_total, e.args[0], e.args[1])}
                return json.dumps(output, indent=2)

            headers_tot = [desc[0] for desc in curs.description]
            rows_tot = curs.fetchall()

            if len(headers) != len(headers_tot): # Must be the same number of columns
                output = {'aaData':[], 'error':'The first query has {} columns and the second has {} columns!'
                    .format(len(headers), len(headers_tot))}
                return json.dumps(output, indent=2)

            headers_len = len(headers)
            rows_max_size = max(len(rows), len(rows_tot))
            calc_rows = []

            for i in range(rows_max_size):
                r1 = rows[i:i+1]
                r2 = rows_tot[i:i+1]
                if not r1:
                    r1 = [' ' for i in range(headers_len)]
                else:
                    r1 = r1[0]
                if not r2:
                    r2 = [' ' for i in range(headers_len)]
                else:
                    r2 = r2[0]
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


    @cherrypy.expose
    def error(self, **args):
        """
        The error page.
        """
        logFull('CeReports:error')
        output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
        return output.render(title='Error 404', links=[], msg='Sorry, this page does not exist!')


    @cherrypy.expose
    def default(self, **args):
        """
        The error page.
        """
        logFull('CeReports:default')
        output = Template(filename=TWISTER_PATH + '/server/template/rep_error.htm')
        return output.render(title='Error 404', links=[], msg='Sorry, this page does not exist!')


# Eof()
