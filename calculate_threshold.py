#!/bin/env python
"""
calculate_threshold.py
by Fred Ross, <fred.ross@epfl.ch>
May 19, 2011

Given a CSV file in which the third field consists of pileups, calculate a threshold for deciding that a single position is not noise with a given type I error rate.

Works by fitting a Poisson distribution to the number of zero, one, two, and other low order pileups.
"""
import os
import sys
import csv
import math
import getopt

usage = """Usage: calculate_threshold.py [-h] [-a alpha] pileup.txt

-h     Print this message and exit
alpha  Calculate threshold with probability alpha of type I error (default 0.05)
pileup CSV file of the pileups (chromosome,position,count)
"""

class Usage(Exception):
    def __init__(self,  msg):
        self.msg = msg

def histogram(values):
    h = {}
    for v in values:
        if not(h.has_key(v)):
            h[v] = 1
        else:
            h[v] += 1
    return h

def main(argv=None):
    alpha = 0.05
    if argv is None:
        argv = sys.argv[1:]
    try:
        try:
            opts, args = getopt.getopt(argv, "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                print usage
                sys.exit(0)
            elif o in ("-p",):
                try:
                    alpha = float(a)
                    if alpha <= 0 or alpha >= 1:
                        raise Usage("Alpha must be between 0 and 1")
                except ValueError, v:
                    raise Usage("Alpha must be a number between 0 and 1")
            else:
                raise Usage("Unhandled option: " + o)

        if len(args) != 1:
            raise Usage("calculate_threshold.py takes exactly one argument.")

        [pileup] = args

        if not(os.path.exists(pileup)):
            raise Usage("Pileup file %s does not exist" % pileup)

        with open(pileup) as f:
            r = csv.reader(f)
            h = histogram([float(c) for a,b,c in r])
            s = []
            
            if h[1] != 0:
                s.append(2*h[2] / float(h[1]))
            if h[2] != 0:
                s.append(3*h[3] / float(h[2]))
            m = s / float(n)
            print m
            # calculate threshold for alpha
        sys.exit(0)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, usage
        return 2
    

if __name__ == '__main__':
    sys.exit(main())
