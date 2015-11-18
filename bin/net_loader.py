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

host_val = "";
port_val = 0;
max_nums = 0;

class Runner( threading.Thread ):
    def setHost( self, host ):
        self._host = host;

    def setPort( self, port ):
        self._port = port;
    def run( self ):
        syslog.syslog( syslog.LOG_INFO, "Ident:%s\tHost:%s\tPort:%d" % ( self.getName(),  self._host, self._port ));
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
    for i in range( 1, max_nums ):
        progress.update( i );
        #t = threading.Thread( target=runner, args=( host_val, port_val) );
        t = Runner();
        t.setHost( host_val );
        t.setPort( port_val );
        t.start();
        time.sleep( 0.05 );
    progress.finish();

    syslog.closelog();
    pass;

