import os
import sys
from BasePlugin import BasePlugin
import base64
import getopt
import getpass
import logging
import string
import time
from datetime import datetime
import urllib
from suds.client import Client
from suds import sudsobject
from suds.sax.text import Text

#

# The proxy object for the JIRA server
soap = None
# The authentication token
auth = None

#

class Plugin(BasePlugin):

    """
    Jira Plugin parameters:

    """

    def run(self, args):
        global soap, commands

        progname = sys.argv[0]
        commands = Commands()  

        logger = MockLogger()

        if 'command' not in args.keys():
            logger.error("No Jira command given.")
            return False

        command_name = args['command']

        jira_env = {}

        if commands.has(command_name):
            
            if command_name in ['login']:
                if 'user' not in args.keys():
                    logger.error("User name was not provided.")           
                    return False

                if 'passwd' not in args.keys():
                    logger.error("Password not provided for %s." %user)           
                    return False

            if 'server' not in args.keys():
                jira_env['server'] = "http://localhost:8080"
                logger.debug("Server was not provided, using local server as default")
            else:
                jira_env['server'] = args['server']
            jira_env['server'] = jira_env['server'] + "/rpc/soap/jirasoapservice-v2?wsdl"

            if not jira_env['server'].startswith('http'):  # also catches https
                jira_env['server'] = 'http://' + jira_env['server'] # default is no SSL   

            try:
                logger.debug('Attempting to connect to the server: ' + jira_env['server'])
                soap = Client(jira_env['server'])
                # for i in soap.sd:
                #     print(i.description())
                
                logger.debug('Connected to the server')
                # logger.debug(soap)
            except:
                logger.error('Failed to connect to: ' + jira_env['server'])
                return False
            # This doesn't actually check that the session is valid
            serverInfo = soap.service.getServerInfo(auth)
            # logger.debug("Server info: " + str(serverInfo))

            home = "notset"
            try:
                home = os.path.expanduser('~'+self.user)
                logger.debug('Set Jira HOME to '+ home)
            except KeyError:
                try:
                    home = os.environ['APPDATA'] + os.sep + "JiraCLI"
                except KeyError:
                    print "Warning: unable to find HOME or APPDATA to store .jirarc file"
                print "Warning: you will need to log into JIRA for every operation"
            if home != "notset" and not os.path.exists(home):
                os.makedirs(home)

            jira_env['home'] = home

            return start_login(jira_env, command_name, logger, args)            

        else:
            logger.error("Command '%s' not recognized." % (command_name))
            logger.error("  run '%s help' for a list of commands" % (progname))
            return False

class JiraCommand(object):

    name = "<default>"
    aliases = []
    summary = "<--- no summary --->"
    usage = ""
    mandatory = ""

    commands = None

    def __init__(self, commands):
        self.commands = commands

    def run(self, logger, jira_env, args):
        """Return a non-zero object for success"""
        return 0

    def render(self, logger, jira_env, results):
        if not results:
            return "empty"
        res = list()
        if type(results) is list:
            for i, v1 in enumerate(results):
                res.append(self.renderElement(v1))
        else:
            res.append(self.renderElement(results))
        return res

    def renderElement(self, item):
        item_lvl1 = {}
        for (k1, val1) in sudsobject.items(item):
            if val1 and type(val1) is list:                    
                l = list()
                for i, v2 in enumerate(val1):                        
                    if isinstance(v2,sudsobject.Object):
                        item_lvl2 = {}
                        for (k2, val2) in sudsobject.items(v2):
                            item_lvl2[k2]=encode(val2)
                        l.append(item_lvl2)
                    else:
                        l.append(encode(v2))
                item_lvl1[k1]=l
            else:
                item_lvl1[k1]=encode(val1)
        return item_lvl1

class JiraGetAttach(JiraCommand):

    name = "getattach"
    summary = "Get attachments of an issue"
    usage = """
    <issue key>           Issue identifier, e.g. CA-1234
    """

    def run(self, logger, jira_env, args):
        global soap, auth
        
        if "key" not in args.keys():
            logger.error("You should provide the issue key")
            return "error"

        issueKey = args["key"]
        logger.debug('Attachments of issue ' + issueKey)
        
        try:
            #  this operation assumes that the user has permissions to get the attachments 
            # TODO add permission check
            results = soap.service.getAttachmentsFromIssue(auth, issueKey)            
            if len(results)>0:
                # print self.render(logger,jira_env,results)            
                return results                         
            else:
                # print "returned empty"
                return "empty"
        except Exception, e:
            logger.error(e)
            return "error"

class JiraAttach(JiraCommand):

    name = "attach"
    summary = "Attach a file to an issue"
    usage = """
    <issue key>           Issue identifier, e.g. CA-1234 
    <attachments>            The attachment objects to manage (as list)
    """

    def run(self, logger, jira_env, args):
        global soap, auth
        if "key" not in args.keys():
            logger.error(self.usage)
            return "error"
        if "attachments" not in args.keys():
            logger.error(self.usage)
            return "nothing to attach"
        issueKey = args["key"]
        attachments = args["attachments"] # this should be a list

        attachSuccessful = True

        for att in attachments:
            filename = att["filename"]
            name = att["filename"]
            path = att["path"]
            filepath = os.path.join(path,filename)
            if not os.path.exists(filepath):
                logger.debug("The path "+filepath+" does not exist")
                return False

            fp = open(filepath, 'rb')
            file_contents = fp.read()
            fp.close()
            file_contents = file_contents.encode('base64')
            name = name.encode("utf-8")

            try:
                results = soap.service.addBase64EncodedAttachmentsToIssue(auth,
                                                            issueKey, 
                                                            [name], 
                                                            [file_contents])
                if not results:
                    logger.debug("Attaching "+name+" failed.")
                    return False

            except Exception, e:
                logger.error(e)
                return False

        try:
            remoteAttachments = commands.run("getattach",logger,jira_env,{"key":issueKey})
            if type(remoteAttachments) is not str:
                return True
            else:
                logger.error("There was an error getting attachments for issue "+issueKey)
                return False
        except Exception, e:
            logger.error(e)
            return False


class JiraUpdateComment(JiraCommand):

    name = "editcomment"
    summary = "Update a comment"
    usage = """
    <issue key>           Issue identifier, e.g. CA-1234
    <text>                Text of the comment
    """
    def run(self, logger, jira_env, args):        
        
        RemoteComment = dict()
        for field in ['id','body']:                                
            newValue = args[field]
            RemoteComment[field]=newValue

        try:
            if soap.service.hasPermissionToEditComment(auth,RemoteComment):
                results = soap.service.editComment(auth,RemoteComment)
                return self.render(logger, jira_env,results)
            else:
                return "You don't have permission to edit this comment"
            
        except Exception, e:
            print(e)
            logger.error(e)
            return "Comment update failed"
        

class JiraComment(JiraCommand):

    name = "comment"
    summary = "Add a comment to an issue"
    usage = """
    <issue key>           Issue identifier, e.g. CA-1234
    <text>                Text of the comment
    """
    def run(self, logger, jira_env, args):
        global soap, auth
        issueKey = args['key']
        message = args['body']
        try:
            # TODO may have to do it this way with Python 2.6?
            # comment = client.factory.create('ns0:RemoteComment')
            # comment.body = 'This is a comment'
            soap.service.addComment(auth, issueKey, {"body":message})
            return ["Comment create successful"]
        except Exception, e:
            print(e)
            logger.error(decode(e))
            return ["Comment create failed"]

class JiraComments(JiraCommand):

    name = "comments"
    summary = "Show all the comments about an issue"
    usage = """
    <issue key>           Issue identifier, e.g. CA-1234
    """
    def run(self, logger, jira_env, args):
        global soap, auth
        if "key" not in args.keys():
            logger.error("You should provide the issue key")
            return "error"

        issueKey = args["key"]
        
        logger.debug('Comments of issue ' + issueKey)
        try:
            results = soap.service.getComments(auth, issueKey)
            # print self.render(logger,jira_env,results)
            if len(results)>0:
                return self.render(logger,jira_env,results)                
            else:
                return "empty"
        except Exception, e:
            print(e)
            logger.error(decode(e))
            return "error"

class JiraCreate(JiraCommand):

    name = "create"
    summary = "Create an issue"
    usage = """

    """

    def run(self, logger, jira_env, args):
        global soap, auth
        remoteIssue = dict()
        
        issue = args['issue']    
        # check for attachments and comments and store them separately
        # until the issue is created
        # we'll deal with adding them later, since for adding/editing them
        # we need the issue key
        # attachments = []
        if 'attachments' in issue.keys():            
            # attachments = issue['attachments'] # this should be a list            
            issue.pop('attachments')
            # print attachments
        # comments = []
        # if 'comments' in issue.keys():
        #     comments = issue['comments'] # this should be a list
        #     issue.pop('comments')
        #     print comments
        # create the issue
        for (field,item) in issue.items():                    
            if field in ['components','fixVersions','affectsVersions']:
                item_list = []
                for i, v in enumerate(item):
                    item_list.append({'id': v["id"]})
                remoteIssue[field] = item_list
            else:
                if field in ['duedate']:
                    val = item
                    if val == 'None':
                        remoteIssue[field]=""
                    else:
                        date = datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                        remoteIssue[field]='{0}T00:00:00.0'.format(date.strftime("%Y-%m-%d"))                    
                else:
                    remoteIssue[field] = item
        
        try:
            newIssue = soap.service.createIssue(auth, remoteIssue)

            if newIssue:
                print newIssue
                return self.render(logger, jira_env, newIssue)

        except Exception, e:       
            print(e)             
            logger.error(e)
            # logger.error(decode(e))
            return "error"

class JiraGetAvailableActions(JiraCommand):

    name = "actions"
    summary = "Get the available actions for this issue"
    usage = """
    <issue key>           Issue identifier, e.g. CA-1234
    """

    def run(self, logger, jira_env, args):
        global soap, auth
        
        issueKey = args['key']
        logger.debug('Actions for issue ' + issueKey)
        try:
            results = soap.service.getAvailableActions(auth, issueKey)
            # print self.render(logger,jira_env,results)
            if len(results)>0:
                return self.render(logger,jira_env,results)
            else:
                return "empty"
        except Exception, e:
            print(e)
            logger.error(decode(e))
            return "error"

def changeStatus(issueKey, logger, jira_env, actionId):
    """Generic function for changing the status of an issue"""
    global soap, auth
    # TODO using defaults for resolution and timetracking but should
    # accept values from args too
    resolution = '1'
    timetracking = '1m'
    try:
        return soap.service.progressWorkflowAction(auth, issueKey, actionId, [
            {"id": "assignee", "values": [jira_env['jirauser']]},
            {"id": "resolution", "values": [resolution]},
            {"id": "timetracking", "values": [timetracking]},
            ])
    except Exception, e:
        print e
        logger.error(decode(e))


class JiraLogin(JiraCommand):

    name = "login"
    summary = "Login to JIRA"
    usage = """
    [userid]         Use a different userid to login to JIRA
    """

    def run(self, logger, jira_env, args):
        global soap, auth
        print args['command']
        if args['command'] not in ['login']:
            logger.error("Previous authorization is invalid or has expired")
            logger.error("You should login again")
            return "Session timeout"
        if 'user' not in args.keys():
            logger.error("Username is not defined")
            return False
        if 'passwd' not in args.keys():
            logger.error("Password is not defined")
            return False
        jirauser = args['user']
        password = args['passwd']
        try:
            logger.info('Attempting to obtain authentication token')
            auth = soap.service.login(jirauser, password)
            logger.info('Done.')        
            # Write the authentication token (not password) to a file
            # for use next time
            jirarc_file = jira_env['home'] + os.sep + '.jirarc'
            fp = open(jira_env['jirarc_file'], 'wb')
            fp.write(jirauser + '\n')
            fp.write(auth + '\n')
            fp.close()
            if hasattr(soap, 'getProjects'):
                # Up to 3.12
                jira_env['projects'] = soap.service.getProjects(auth)
            else:
                jira_env['projects'] = soap.service.getProjectsNoSchemes(auth)               
            return self.render(logger,jira_env,jira_env['projects'])
        except Exception, e:
            logger.error("Login failed")
            logger.error(e)


class JiraLogout(JiraCommand):

    name = "logout"
    summary = "Log out of JIRA before the session is timed out"
    usage = """
    """

    def run(self, logger, jira_env, args):
        global soap, auth
        if len(args) > 0:
            logger.error(self.usage)
            return 0
        try:
            auth = soap.service.logout(auth)
            # Delete the authentication token (not password) from a file
            jirarc_file = jira_env['home'] + os.sep + '.jirarc'
            if os.path.exists(jirarc_file):
                os.remove(jirarc_file)
            return 1
        except Exception, e:
            logger.exception(e)
            logger.error("Logout failed")

class JiraGetIssues(JiraCommand):

   name = "getissues"
   summary = "List issues that match a JQL query. Shows issue key, created and summary fields sorted by created. Requires JIRA 4.x"
   usage = """
   "<JQL query>"             JQL query, e.g. "Summary ~ '%some%text%' AND Reporter=nagios AND Created > -7d"
   [<limit>]                   Optional limit to number of issues returned, default 100 
   """

   def run(self, logger, jira_env, args):
        global soap, auth
        if 'query' not in args.keys():
            logger.error(self.summary)
            logger.error(self.usage)
            return False
        else:
            query = args['query']
        if 'limit' in args.keys():           
            limit = args['limit']
        else:
            limit = 100
        issues = soap.service.getIssuesFromJqlSearch(auth, query, limit)    
        if len(issues)==0:
            logger.debug('No issues found to match the query '+query)     
            return "empty"
        else:                
            # Attempt to get attachments for issues:
            # it is also possible to get the comments here, 
            # but this operation is currently implemented separately 
            # at request from the Java interface
            for issue in issues:
                # try:
                #     comments = soap.service.getComments(auth, issue["key"])
                #     if len(comments)>0:
                #         # print comments
                #         issue["comments"]=comments
                # except Exception, e:
                #     logger.error("Failed to get comments for issue "+issue["key"])

                try:
                    attachments = soap.service.getAttachmentsFromIssue(auth, issue["key"])
                    if len(attachments)>0:
                        # print attachments
                        issue["attachments"]=attachments
                except Exception, e:
                    logger.error("Failed to get attachments for issue "+issue["key"])
                
            # print(self.render(logger,jira_env,issues))
            return self.render(logger,jira_env,issues)


class JiraListUsers(JiraCommand):

    name = "listusers"
    summary = "List users, needs administrator permission"
    usage = """
    """
    
    def run(self, logger, jira_env, args):
        global soap, auth
        try:
           groupname = "jira-users"
           group = soap.service.getGroup(auth, groupname)
           return group['users']
        except Exception, e:
            logger.exception(e)

    def render(self, logger, jira_env, args, results):
       def compare(a, b):
          if a == None:
             return b
          if b == None:
             return a
          return cmp(a['fullname'], b['fullname'])
       for user in sorted(results, compare):
          if user['name'] not in ['authad']:
             logger.info("%s,%s,%s" % (user['name'], user['fullname'], user['email']))
       logger.info("%d users" % len(results))
       return 0

class JiraGetVersions(JiraCommand):

    name = "getversions"
    summary = "Get versions for a particular project, identified by project key"
    usage = """
    <source project>              Project key, e.g. TSTONE
    """
    
    def run(self, logger, jira_env, args):
        global soap, auth
        
        if 'project' not in args.keys():
            logger.error(self.summary)
            logger.error(self.usage)
            return "error"
        src_project = args['project']
        logger.debug('Getting versions for project '+src_project)     
        try:
            src_versions = soap.service.getVersions(auth, src_project)
            if len(src_versions)==0:
                logger.debug('No versions defined for project '+src_project)     
                return "empty"
            else:
                # print(self.render(logger,jira_env,src_versions))
                return self.render(logger,jira_env,src_versions)
        except Exception, e:
            logger.debug(e)
            return "error"


class JiraGetComponents(JiraCommand):

    name = "getcomponents"
    summary = "Get components for a particular project, identified by project key"
    usage = """
    <source project>              Project key, e.g. TSTONE
    """
    
    def run(self, logger, jira_env, args):
        global soap, auth
        
        if 'project' not in args.keys():
            logger.error(self.summary)
            logger.error(self.usage)
            return "error"
        src_project = args['project']
        logger.debug('Getting components for project '+src_project)        
        try:
            src_components = soap.service.getComponents(auth, src_project)
            if len(src_components)==0:
                logger.debug('No components defined for project '+src_project)        
                return "empty"
            else:
                return self.render(logger,jira_env,src_components)
        except Exception, e:
            logger.debug(e)
            # logger.exception(e)
            return "error"

class JiraGetIssueTypes(JiraCommand):

    name = "getissuetypes"
    summary = "Get issue types"
    usage = """
    no arguments
    """
    
    def run(self, logger, jira_env, args):
        global soap, auth
        
        try:
            issue_types = soap.service.getIssueTypes(auth)
            if len(issue_types)==0:
                logger.debug('Unable to get issue types!')        
                return "empty"
            else:
                # print(self.render(logger,jira_env,issue_types))
                return self.render(logger,jira_env,issue_types)
        except Exception, e:
            logger.debug(e)
            # logger.exception(e)
            return False

class JiraGetPriorities(JiraCommand):

    name = "getpriorities"
    summary = "Get priority types"
    usage = """
    no arguments
    """
    
    def run(self, logger, jira_env, args):
        global soap, auth
        
        try:
            priority_types = soap.service.getPriorities(auth)
            if len(priority_types)==0:
                logger.debug('Unable to get priority types!')        
                return "empty"
            else:
                # print(self.render(logger,jira_env,priority_types))
                return self.render(logger,jira_env,priority_types)
        except Exception, e:
            logger.debug(e)
            # logger.exception(e)
            return False


class JiraGetStatuses(JiraCommand):

    name = "getstatuses"
    summary = "Get statuses"
    usage = """
    no arguments
    """
    
    def run(self, logger, jira_env, args):
        global soap, auth
        
        try:
            statuses = soap.service.getStatuses(auth)
            if len(statuses)==0:
                logger.debug('Unable to get statuses!')        
                return "empty"
            else:
                # print(self.render(logger,jira_env,statuses))
                return self.render(logger,jira_env,statuses)
        except Exception, e:
            logger.debug(e)
            # logger.exception(e)
            return False  

class JiraGetResolutionTypes(JiraCommand):

    name = "getresolutions"
    summary = "Get resolution types"
    usage = """
    no arguments
    """
    
    def run(self, logger, jira_env, args):
        global soap, auth
        
        try:
            res_types = soap.service.getResolutions(auth)
            if len(res_types)==0:
                logger.debug('Unable to get resolution types!')        
                return "empty"
            else:
                return self.render(logger,jira_env,res_types)                
        except Exception, e:
            logger.debug(e)
            # logger.exception(e)
            return False    


class JiraUpdate(JiraCommand):

    name = "update"
    summary = "Update the contents of an issue"
    usage = """
    <issue key>           Issue identifier, e.g. CA-1234
    <field>               Name of field to update
    <value>               New value or comma-separated values for the field
    """

    def run(self, logger, jira_env, args):
       
        issue = args['issue']
        issueKey = issue["key"]
        
        # change the status of the issue
        statAction = issue['status']
        changeStatus(issueKey, logger, jira_env, statAction)
        issue.pop('status')
        
        # save attachments and comments to treat separately
        # attachments = []        
        if 'attachments' in issue.keys():
            # attachments = issue['attachments']
            issue.pop('attachments')
        # comments = []        
        # if 'comments' in issue.keys():
        #     comments = issue['comments']
        #     issue.pop('comments')

        # create list of parameters to update
        paramList = list()
        for (field,newValue) in issue.items():                  
            if field in ['affectsVersions', 'fixVersions', 'components']:
                val = newValue # for these fields are lists of dictionaries 
                # -> should get only the id's as a list of strings
                newValue = list()
                for (i,v) in enumerate(val):
                    newValue.append(v['id'])        
            if field in ['affectsVersions']:
                field = 'versions'        
            if field in ['duedate', 'created', 'updated']:
                val = newValue
                if val=='None':
                    newValue = ""
                else:
                    date = datetime.strptime(newValue, "%Y-%m-%d %H:%M:%S")
                    newValue=[format(date.strftime("%d/%b/%y"))]                    
            if type(newValue) is not list:
                newValue = [newValue]
            paramList.append({'id':field,'values':newValue})
        try: # attempt to update the isse
            remoteIssue = soap.service.updateIssue(auth, issueKey, paramList)

            if remoteIssue:
                # key = remoteIssue["key"]
                # logger.debug('updated issue '+key)
                # attNames = []                
                # if attachments:
                #     attachSuccessful = True
                #     for att in attachments: # att should be a dictionary
                #         # check if there's any action to be performed on this attachment
                #         if 'status' in att.keys():
                #             status = att['status']
                #             att["key"] = key
                #             if status in ['upload']:
                #                 flag = commands.run('attach', logger, jira_env, att)
                #             elif status in ['download']:
                #                 pass 
                #             elif status in ['delete']:
                #                 pass
                #             if flag:
                #                 att.pop('status') # there's no action to be performed on this attachment
                #                 attNames.append(att['filename'])
                #             else:
                #                 attachSuccessful = False
                #     if attachSuccessful:
                #         remoteIssue['attachmentNames'] = attNames
                #         remoteAttachments = commands.run("getattach",logger,jira_env,{"key":key})
                #         if type(remoteAttachments) is not str: # the 'getattach' command might return "empty" or "error"
                #             remoteIssue['attachments'] = remoteAttachments

                # print remoteIssue 
                return self.render(logger, jira_env, remoteIssue)
            else:
                print "error"
                return "error"
        except Exception, e:                
            print "error"
            print e
            logger.error(e)            
            return "error"


class JiraUnitTest(JiraCommand):

    name = "test"
    summary = "Run unit tests on the JIRA CLI"
    usage = """
    """

    def run(self, logger, jira_env, args):
       import doctest
       global soap, auth
       if len(args) != 0:
          logger.error(self.usage)
          return 0
       logger = MockLogger()
       logger.debug('Running unit tests ...')
       globs = { 'com': com,
                 'logger': logger,
                 'jira_env': jira_env,
                 'args': args,
                 }
       verbosity = False
       if options.loglevel < logging.INFO:
          verbosity = True
       doctest.testfile("../test/cli/CliTests.log", verbose=verbosity, extraglobs = globs, optionflags = doctest.REPORT_UDIFF)
       logger.debug('Finished unit tests')


class Commands:

    def __init__(self):
        self.commands = {}
        self.add(JiraAttach)
        self.add(JiraGetAttach)        
        self.add(JiraComment)
        self.add(JiraUpdateComment)
        self.add(JiraComments)
        self.add(JiraCreate)
        self.add(JiraListUsers)
        self.add(JiraLogin)
        self.add(JiraLogout)        
        self.add(JiraGetIssues)
        self.add(JiraGetComponents)
        self.add(JiraGetVersions)
        self.add(JiraUnitTest)
        self.add(JiraUpdate)
        self.add(JiraGetIssueTypes)
        self.add(JiraGetPriorities)
        self.add(JiraGetStatuses)
        self.add(JiraGetResolutionTypes)
        self.add(JiraGetAvailableActions)

    def add(self, cl):
        # TODO check for duplicates in commands
        c = cl(self)
        self.commands[c.name] = c
        for a in c.aliases:
            self.commands[a] = c

    def has(self, command):
        return self.commands.has_key(command)

    def run(self, command, logger, jira_env, args):
        """Return the exit code of the whole process"""
        return self.commands[command].run(logger, jira_env, args)

    def getall(self):
        keys = self.commands.keys()
        keys.sort()
        return map(self.commands.get, keys)

def encode(s):
    '''Deal with unicode in text fields'''
    if s == None:
        return "None"
    if type(s) == unicode:
        s = s.encode("utf-8")
    return str(s)

def dateStr(i):
    '''Convert a datetime or String object to a string output format'''
    if i == None or i == 'None':
        return str(i)
    # JIRA 4.4 returns a datetime object
    if hasattr(i, 'date'):
        return "%04d/%02d/%02d %02d:%02d:%02d" % (i.year, i.month, i.day, i.hour, i.minute, i.second)
    return "%04d/%02d/%02d %02d:%02d:%02d" % (i[0], i[1], i[2], i[3], i[4], i[5])

def getName(id, fields):
    '''TODO cache this, and note getCustomFields() needs admin privilege'''
    if id == None:
        return "None"
    if fields == None:
        return id
    for i, v in enumerate(fields):
        val = v['id']
        if val and val.lower() == id.lower():
            return v['name']
    return id.title()
            
def decode(e):
    """Process an exception for useful feedback"""
    # TODO how to log the fact it is an error, but allow info to be unchanged?
    # TODO now fault not faultstring?
    # The faultType class has faultcode, faultstring and detail
    str = e.faultstring
    if str == 'java.lang.NullPointerException':
        return "Invalid issue key?"
    return e.faultstring
    

def setupLogging(loglevel=logging.INFO):
    """Set up logging, by default just echo to stdout"""
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(loglevel)
    # TODO logging.getLogger('suds.client').setLevel(logging.DEBUG), suds.transport etc
    formatter = logging.Formatter("%(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

class MockLogger:
   """Print the output to stdout for doctest to check."""
   def __init__(self): pass
   def info(self, s): print (s)
   def warning(self, s): print (s)
   def debug(self, s): print (s)
   def error(self, s): print (s)

def start_login(jira_env, command_name, logger, args):
    global auth
    # Attempt to login or recover the cached auth object
    jirarc_file = jira_env['home'] + os.sep + '.jirarc'
    jira_env['jirarc_file'] = jirarc_file
    # print(jirarc_file)
    while not auth:
        try:
            logger.debug('Starting authorization')
            # Allow an explicit login, to reset the user for example
            if command_name == 'login' and os.path.exists(jirarc_file):
                os.remove(jirarc_file)
            if not os.path.exists(jirarc_file):
                logger.debug('No cached auth, starting login')                
                rc = commands.run('login', logger, jira_env, args)                
                return rc
            logger.debug('Reading cached auth')
            fp = open(jirarc_file, 'rb')
            jira_env['jirauser'] = fp.readline()[:-1]
            auth = fp.readline()[:-1]
            fp.close()            
          	    
        except Exception, e:
            # Attempt another login
            logger.error('Previous login is invalid or has expired')
            if os.path.exists(jirarc_file):
                os.remove(jirarc_file)            

    rc = commands.run(command_name, logger, jira_env, args)
    if (rc):
        return rc          
