
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

# Status translations :

execStatus = {'stopped':STATUS_STOP, 'paused':STATUS_PAUSED, 'running':STATUS_RUNNING, 'resume':STATUS_RESUME,
	'invalid':STATUS_INVALID}

testStatus = {'pending':STATUS_PENDING, 'working':STATUS_WORKING, 'pass':STATUS_PASS, 'fail':STATUS_FAIL,
	'skipped':STATUS_SKIPPED, 'aborted':STATUS_ABORTED, 'not executed':STATUS_NOT_EXEC, 'timeout':STATUS_TIMEOUT,
	'invalid':STATUS_INVALID, 'waiting':STATUS_WAITING}

# FWM-Config XML Tags :

FWMCONFIG_TAGS = (
	{'name':'EpNames',		'tag':'EpNames',			'default':''},
	{'name':'TestsPath',	'tag':'TestCaseSourcePath',	'default':''},
	{'name':'LogsPath',		'tag':'LogsPath',			'default':''},
	{'name':'DbConfig',		'tag':'DbConfigFile',		'default':''},
	{'name':'EmailConfig',	'tag':'EmailConfigFile',	'default':''},
	{'name':'GlobalParams',	'tag':'GlobalParams',		'default':''},
)

# Project Config XML Tags :

PROJECTCONFIG_TAGS = (
	{'name':'ExitOnTestFail', 'tag':'stoponfail',		'default':False, 'type':'bool'},
	{'name':'DbAutoSave',	'tag':'dbautosave',			'default':False, 'type':'bool'},
	{'name':'TestcaseDelay', 'tag':'tcdelay',			'default':0, 'type':'number'},
	{'name':'Libraries',	'tag':'libraries',			'default':''},
	{'name':'ScriptPre',	'tag':'ScriptPre',			'default':''},
	{'name':'ScriptPost',	'tag':'ScriptPost',			'default':''},
)

# Suites Tags, from Project Config XML :

SUITES_TAGS = (
	{'name':'name',			'tag':'tsName',				'default':''},
	{'name':'tb',			'tag':'TbName',				'default':''},
	{'name':'pd',			'tag':'PanicDetect',		'default':''},
	{'name':'libraries',	'tag':'libraries',			'default':''},
)

# Tests Tags, from Project Config XML :

TESTS_TAGS = (
	{'name':'file',			'tag':'tcName',				'default':''},
	{'name':'dependancy',	'tag':'Dependancy',			'default':''},
)
