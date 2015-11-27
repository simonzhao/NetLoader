#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys;
reload( sys );
sys.setdefaultencoding( 'utf8' );

import getopt;
import progressbar;
import time;
import threading;
import syslog;
import socket;
import uuid;
import random;
import websocket;
import multiprocessing;
import os;

host_val = "";
port_val = 0;
max_nums = 0;
process_nums = 0;
threads_nums = 0;

#class Runner( threading.Thread ):
class Runner( multiprocessing.Process ):
    def setHost( self, host ):
        self._host = host;

    def setPort( self, port ):
        self._port = port;

    def getName( self ):
        return "Process-" + str( os.getpid() );

    def run( self ):
        #print "进程%d\t线程%s" % ( os.getpid(), self.getName() );
        self.__waitTime = 0;
        self.__runNums = 0;
        self.__runTime = 0;

        w = random.uniform(0, 2);
        syslog.syslog( syslog.LOG_INFO, "Ident:%s\tWait:%f" % ( self.getName(), w ));
        time.sleep( w );
        syslog.syslog( syslog.LOG_INFO, "Ident:%s\tHost:%s\tPort:%d" % ( self.getName(),  self._host, self._port ));

        runStartTime = time.time();
        conn = websocket.create_connection( "ws://%s:%d/" % ( self._host, self._port ) );
        connPayTime = time.time() - runStartTime;
        queryPayTimes = [];
        #conn = socket.socket();
        try:
            #conn.connect( ( self._host, self._port ) );
            for i in xrange( 30 ):
                data = str( uuid.uuid1() );
                startTime = time.time();
                conn.send( data );
                recv = conn.recv( );
                payTime = time.time() - startTime;
                queryPayTimes.append( payTime );
                self.__waitTime = self.__waitTime + payTime;
                self.__runNums += 1;

                syslog.syslog( syslog.LOG_INFO, 'Ident:[%s]\tNo:[%d]\tSend:[%s]\tRecv:[%s]' % ( self.getName(), i, data, recv ) );
                time.sleep( 1 );
        finally:
            conn.close();
            self.__runTime = time.time() - runStartTime;

            maxPayTime = max( queryPayTimes );
            minPayTime = min( queryPayTimes );
            print 'Process:[%d]\tIdent:[%s]\tRun:[%d]\tRunTime:[%f]\tWaitTime:[%.2f]\tMax:[%.3f]\tMin:[%.3f]\tConnectPay:[%.3f]'\
                    % ( os.getpid(), self.getName(), self.__runNums, self.__runTime, self.__waitTime, maxPayTime, minPayTime, connPayTime );
        return;
    pass;

if __name__ == "__main__":
    options, args = getopt.getopt(
            sys.argv[ 1: ],
            "h",
            [
                "help",
                "host=", #待测试的服务器IP
                "port=", #服务器端口
                "process=", #并发进程数
                "threads=", #每个进程控制的线程数
                ]
            );
    for name, value in options:
        print "name:%s\tval:%s" % ( name, value );
        if name == '--host':
            host_val = value;
        elif name == '--port':
            port_val = int( value );
        elif name == '--process':
            process_nums = int( value );
        elif name == '--threads':
            threads_nums = int( value );

    #syslog.openlog( 'NetLoader', syslog.LOG_PID | syslog.LOG_PERROR, syslog.LOG_LOCAL4 );
    syslog.openlog( 'NetLoader', syslog.LOG_PID, syslog.LOG_LOCAL4 );

    max_nums = threads_nums * process_nums;
    print "测试服务器[%s:%d], 最大连接数:[%d]" \
            % ( host_val, port_val, max_nums );

    ps = [];
    for i in range( 0, process_nums ):
        """
        child_pid = os.fork();
        if child_pid == 0:
            print "创建子进程";
            worker();
        elif child_pid > 0:
            print "父进程";
        """
        p = Runner();
        p.setHost( host_val );
        p.setPort( port_val );
        p.start();
        ps.append( p );
        pass;
        
    print  "\n\n====================================================";
    for p in ps:
        p.join();
    print  "\n\n测试结束";
    pass;

