
# version: 2.013

# Major list of constants.

# Central Engine and Execution Process statuses:

STATUS_STOP    = 0 # Suicide; the test suite is immediately killed
STATUS_PAUSED  = 1 # After the current test is finished, the suite is frozen
STATUS_RUNNING = 2 # The suite is running
STATUS_RESUME  = 3 # Continue the paused tests
STATUS_INVALID = 8 # Invalid status

# Test statuses :

STATUS_PENDING  = 10 # Not yet run, waiting to start
STATUS_WORKING  = 1  # Is running now
STATUS_PASS     = 2  # Test is finished successful
STATUS_FAIL     = 3  # Test failed
STATUS_SKIPPED  = 4  # When file doesn't exist, or test has flag `runnable = False`
STATUS_ABORTED  = 5  # When test is stopped while running
STATUS_NOT_EXEC = 6  # Not executed, is sent from TC when tests are paused, and then stopped instead of being resumed
STATUS_TIMEOUT  = 7  # When timer expired
STATUS_INVALID  = 8  # When timer expired, the next run
STATUS_WAITING  = 9  # Is waiting for another test

# List with all available roles

ROLES = [

	'RUN_TESTS',		# Can run tests ? (server + applet)
	'EDIT_TC',			# Can edit test files ? (applet)

	'CREATE_PROJECT',	# Can create new projects ? (applet)
	'CHANGE_PROJECT',	# Can change defined projects ? (applet)
	'DELETE_PROJECT',	# Can delete projects ? (applet)

	'VIEW_REPORTS',		# Can view ? (server + applet)
	'CHANGE_FWM_CFG',	# Can change his main config ? (applet)
	'CHANGE_GLOBALS',	# Can change global parameters ? (applet)
	'CHANGE_DB_CFG',	# Can change database config ? (applet)
	'CHANGE_EML_CFG',	# Can change e-mail config ? (applet)
	'CHANGE_PLUGINS',	# Can load/ unload plugins ? (applet)

	'CHANGE_TESTBED',	# Can change the global testbed ? (server + applet)
	'CHANGE_SUT',		# Can change the global SUT ? (server + applet)
	'CHANGE_SERVICES',	# Can start/ stop services ? (server + applet)
	'CHANGE_USERS',		# Can create, change and delete users ? (server + applet)
]

# Status translations :

execStatus = {'stopped':STATUS_STOP, 'paused':STATUS_PAUSED, 'running':STATUS_RUNNING, 'resume':STATUS_RESUME,
	'invalid':STATUS_INVALID}

testStatus = {'pending':STATUS_PENDING, 'working':STATUS_WORKING, 'pass':STATUS_PASS, 'fail':STATUS_FAIL,
	'skipped':STATUS_SKIPPED, 'aborted':STATUS_ABORTED, 'not executed':STATUS_NOT_EXEC, 'timeout':STATUS_TIMEOUT,
	'invalid':STATUS_INVALID, 'waiting':STATUS_WAITING}

# FWM-Config XML Tags :

FWMCONFIG_TAGS = (
	{'name':'ep_names',		'tag':'EpNames',			'default':''},
	{'name':'tests_path',	'tag':'TestCaseSourcePath',	'default':''},
	{'name':'logs_path',	'tag':'LogsPath',			'default':''},
	{'name':'libs_path',	'tag':'LibsPath',			'default':''},
	{'name':'db_config',	'tag':'DbConfigFile',		'default':''},
	{'name':'eml_config',	'tag':'EmailConfigFile',	'default':''},
	{'name':'glob_params',	'tag':'GlobalParams',		'default':''},
	{'name':'tcfg_path',	'tag':'TestConfigPath',		'default':''},
	{'name':'archive_logs_path', 'tag':'ArchiveLogsPath', 'default': False},
	{'name':'archive_logs_path_active', 'tag':'ArchiveLogsPathActive', 'default': ''},
)

# Project Config XML Tags :

PROJECTCONFIG_TAGS = (
	{'name':'exit_on_test_fail','tag':'stoponfail',			'default':False, 'type':'bool'},
	{'name':'db_auto_save',		'tag':'dbautosave',			'default':False, 'type':'bool'},
	{'name':'tc_delay',			'tag':'tcdelay',			'default':0, 'type':'number'},
	{'name':'libraries',		'tag':'libraries',			'default':''},
	{'name':'script_pre',		'tag':'ScriptPre',			'default':''},
	{'name':'script_post',		'tag':'ScriptPost',			'default':''},
	{'name':'script_mandatory',	'tag':'PrePostMandatory',	'default':False, 'type':'bool'},
	{'name':'clear_case_view',	'tag':'ClearCaseView'	,	'default':''},
)

# Suites Tags, from Project Config XML :

SUITES_TAGS = (
	{'name':'sut',			'tag':'SutName',			'default':''},
	{'name':'name',			'tag':'tsName',				'default':''},
	{'name':'pd',			'tag':'PanicDetect',		'default':''},
	{'name':'libraries',	'tag':'libraries',			'default':''},
)

# Tests Tags, from Project Config XML :

TESTS_TAGS = (
	{'name':'file',			'tag':'tcName',				'default':''},
	{'name':'config_files',	'tag':'ConfigFiles',		'default':''},
	{'name':'dependancy',	'tag':'Dependancy',			'default':''},
	{'name':'clearcase',	'tag':'ClearCase',			'default':''},
)
