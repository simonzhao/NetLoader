#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys;
reload( sys );
sys.setdefaultencoding( 'utf8' );

import getopt;

host_val = "";
port_val = 0;
max_nums = 0;

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

    print "测试服务器[%s:%d], 最大连接数:[%d]" % ( host_val, port_val, max_nums );
    pass;

