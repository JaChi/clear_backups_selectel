#!/usr/bin/env python

import sys, os
import time, datetime
import getopt, ftplib

def helper():
    print ('Usage:  clear_backups.py  [-u username] [-W password] [-p path] [-d days]\
\nOptions:\
\n-u, --user=<string>     Set the username from FTP server \
\n-W, --pass=<string>     Set the username from FTP server \
\n-p, --path=<string>     Path to the container. Default container path \'backups/mif/dbs\'\
\n-d, --days=<number>     Time for which we save backups\
\n-h, --help\
')

def wrLog(msg):
    if not os.path.exists('log'): 
        os.makedirs('log')
    log_file='log/out.log'
    logfile = open(log_file, "a")
    t = time.strftime("%Y-%m-%d %H:%M:%S ")
    logfile.write(t + msg + '\n')
    logfile.close()

def ftpClear(ftp, path, days):
    dtime = time.time()

    try:
        wrLog('INFO :: Go to container ' + path)
        ftp.cwd(path)
    except ftplib.all_errors as e:
        wrLog('ERROR :: ' + str(e) + ' ' + path)
        sys.exit(2)
    
    wrLog('INFO :: Checking the time of the last file change...')
    for i in ftp.nlst():
        t = ftp.sendcmd('MDTM ' + i)
        ftime = time.mktime(datetime.datetime.strptime(t[4:], "%Y%m%d%H%M%S").timetuple())-time.timezone
        if (dtime-ftime) > days*60*60*24:
            fname = path + '/' + i
            wrLog('INFO :: Delete file ' + fname)
            ftp.delete(i)
    wrLog('INFO :: Script has completed')

def main(argv):
    host='ftp://ftp.selcdn.ru'
    user = psw = days =''
    path='backups/mif/dbs'

    wrLog('INFO :: Start sscript...' + '#'*10)

    try:
        opts, args = getopt.getopt(argv,"hu:W:p:d:",["help","user=","pass=","path=","days="])
    except getopt.GetoptError:
        helper()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helper()
            sys.exit()
        elif opt in ("-u", "--user"):
            user = arg
        elif opt in ("-W", "--pass"):
            psw = arg
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-d", "--days"):
            try:
                days = int(arg)
            except:
                wrLog('ERROR :: Invalid days value - ' + arg)
                helper()
                sys.exit()
    if user and psw and days:
        try:
            wrLog('INFO :: Connecting to FTP server...')
            ftp = ftplib.FTP(host,user,psw)
        except ftplib.all_errors as e:
            wrLog('ERROR :: ' + str(e))
            sys.exit(2) 
        ftpClear(ftp,path,days)       
    else:
        helper()
        sys.exit()

main(sys.argv[1:])