
import random
import datetime
import MySQLdb

def populate():
    '''
    release , build , suite , station , test_view
    '''
    #
    conn = MySQLdb.connect(host="11.126.32.9", user="tsc", passwd="tsc", db="testdb")
    curs = conn.cursor()
    curs.execute('TRUNCATE table repo_station')
    curs.execute('TRUNCATE table repo_suite')
    curs.execute('TRUNCATE table repo_release')
    curs.execute('TRUNCATE table repo_build')
    curs.execute('TRUNCATE table repo_test_view')
    #
    for i in range(1, 11):
        curs.execute('INSERT INTO repo_station (name, ip, description) VALUES (%s, %s, %s)',
            ['Workstation %i' % i, '192.168.1.%i' % i, 'Some Workstation'])
    #
    for i in range(1, 21): # Suite
        #
        curs.execute('INSERT INTO repo_suite (name, description) VALUES (%s, %s)',
            ['Suite %i' % i, 'This suite nr %i' % i])
        #
    #
    for r in range(1, 5): # Release
        #
        curs.execute('INSERT INTO repo_release (name, software_ver) VALUES (%s, %s)',
            ['Release %i' % r, str(r)])
        #
    #
    for b in range(1, 101): # Build
        #
        curs.execute('INSERT INTO repo_build (name, release_id, software_ver) VALUES (%s, %s, %s)',
            [ 'Build %i' % b, str(r), '1.'+str(b) ])
        #
    #
    for r in range(1, 5): # Release
        #
        for b in range(1, 101): # Build
            #
            month = b // 12 + 1
            day = (b % 12 + 1) * 2
            #
            for t in range(1, 21):
                # Pass, fail, skip, abort, not exec, timeout
                rnd_status = random.choice(['Pass','Pass','Pass','Pass','Pass','Pass',  'Fail','Fail','Fail','Fail',  'Skip','Abort','Not-exec','Timeout'])
                rnd_suite = str(random.randrange(0, 20))
                rnd_station = str(random.randrange(1, 11))
                #
                curs.execute('INSERT INTO repo_test_view (release_id, build_id, suite_id, station_id, tdate, status) VALUES (%s, %s, %s, %s, %s, %s)',
                    [str(r), str(b), rnd_suite, rnd_station, datetime.datetime(2012, month, day), rnd_status])
                #
            #
    #
    print('Ok! Done!')
    #

if __name__ == '__main__':
    populate()
