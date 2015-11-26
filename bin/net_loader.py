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

host_val = "";
port_val = 0;
max_nums = 0;

class Runner( threading.Thread ):
    def setHost( self, host ):
        self._host = host;

    def setPort( self, port ):
        self._port = port;

    def run( self ):
        self.__waitTime = 0;
        self.__runNums = 0;
        self.__runTime = 0;

        w = random.uniform(0, 2);
        syslog.syslog( syslog.LOG_INFO, "Ident:%s\tWait:%f" % ( self.getName(), w ));
        time.sleep( w );
        syslog.syslog( syslog.LOG_INFO, "Ident:%s\tHost:%s\tPort:%d" % ( self.getName(),  self._host, self._port ));

        runStartTime = time.time();
        conn = websocket.create_connection( "ws://%s:%d/" % ( self._host, self._port ) );
        #conn = socket.socket();
        try:
            #conn.connect( ( self._host, self._port ) );
            for i in xrange( 30 ):
                data = str( uuid.uuid1() );
                startTime = time.time();
                conn.send( data );
                recv = conn.recv( );
                payTime = time.time() - startTime;
                self.__waitTime = self.__waitTime + payTime;
                self.__runNums += 1;

                syslog.syslog( syslog.LOG_INFO, 'Ident:[%s]\tNo:[%d]\tSend:[%s]\tRecv:[%s]' % ( self.getName(), i, data, recv ) );
                time.sleep( 1 );
        finally:
            conn.close();
            self.__runTime = time.time() - runStartTime;
            print 'Ident:[%s]\tRun:[%d]\tRunTime:[%f]\tWaitTime:[%f]' % ( self.getName(), self.__runNums, self.__runTime, self.__waitTime );
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
                "max=", #最大链接数
                ]
            );
    for name, value in options:
        print "name:%s\tval:%s" % ( name, value );
        if name == '--host':
            host_val = value;
        elif name == '--port':
            port_val = int( value );
        elif name == '--max':
            max_nums = int( value );

    syslog.openlog( 'NetLoader', syslog.LOG_PID, syslog.LOG_LOCAL4 );

    print "测试服务器[%s:%d], 最大连接数:[%d]" \
            % ( host_val, port_val, max_nums );

    widgets = [ '测试', progressbar.Percentage(), ' ', progressbar.Bar( marker=progressbar.RotatingMarker('#'))  ];
    progress = progressbar.ProgressBar( widgets= widgets, maxval=max_nums ).start();
    for i in range( 0, max_nums ):
        progress.update( i );
        #t = threading.Thread( target=runner, args=( host_val, port_val) );
        t = Runner();
        t.setHost( host_val );
        t.setPort( port_val );
        t.start();
    progress.finish();

    print  "测试结束";
    #syslog.closelog();
    pass;

