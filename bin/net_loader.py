#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys;
reload( sys );
sys.setdefaultencoding( 'utf8' );

import getopt;

if __name__ == "__main__":
    options, args = getopt.getopt( sys.argv[ 1: ], "h", ["help", "host=", "port=" ] );
    for name, value in options:
        print "name:%s\tval:%s" % ( name, value );
    pass;

