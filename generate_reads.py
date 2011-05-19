#!/bin/env python
"""
generate_reads.py
by Fred Ross, <fred.ross@epfl.ch>
May 19, 2011

Given a FASTA file of sequences and a comma separated file of
sequence,center,amplitude triples, generates single stranded ChipSeq
reads of the given length on the FASTA sequences according to a
background level plus Gaussians of a fixed standard deviation at the
centers and with the amplitudes given in the file.

The amplitude of the Gaussians are measured relative to a background of 1.

The reads are written as sequences, one per line, to the output.
"""
import os
import sys
import csv
import getopt

usage = """Usage: generate_reads.py [-h] [-s stdev] [-L frag_len] [-l read_len] [-o output] [-n n_reads] template.fasta centers.txt

-h              Print this message and exit
-s stdev        The standard deviation to use for the Gaussians (default: 5)
-L frag_len     The mean length of sheared sequence fragments (default: 100)
-l read_len     The length of reads to generate (default: 38)
-o output       File to write to (default: stdout)
-n n_reads      Number of reads to generate (default: 500)
template.fasta  Sequences to write to
centers.txt     CSV file of positions for binding sites
"""

class Usage(Exception):
    def __init__(self,  msg):
        self.msg = msg

def chomp(s):
    while s != "" and (s[-1] == '\n' or s[-1] == '\r'):
        s = s[:-1]
    return s

def read_fasta(filename):
    sequences = {}
    with open(filename) as f:
        current_id = None
        for line in f:
            if line[0] == '>':
                if current_id != None:
                    sequences[current_id] = current_seq
                offset = line.find(' ')
                current_id = line[1:offset]
                current_seq = ""
            elif chomp(line) == "":
                next
            else:
                current_seq = current_seq + chomp(line)
    sequences[current_id] = current_seq
    return sequences


def main(argv=None):
    output = sys.stdout
    read_len = 38
    frag_len = 100
    stdev = 5
    n_reads = 500
    if argv is None:
        argv = sys.argv[1:]
    try:
        try:
            opts, args = getopt.getopt(argv, "hs:L:l:o:n:", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                print usage
                sys.exit(0)
            if o in ("-s",):
                try:
                    stdev = int(a)
                    if stdev < 1:
                        raise ValueError("Stdev must be negative")
                except ValueError, v:
                    raise Usage("Argument to -s must be a positive integer.")
            if o in ("-l",):
                try:
                    read_len = int(a)
                    if read_len < 1:
                        raise ValueError("Read length must be positive")
                except ValueError, v:
                    raise Usage("Argument to -l must be a positive integer.")
            if o in ("-L",):
                try:
                    frag_len = int(a)
                    if frag_len < read_len:
                        raise Usage("Fragment length must be no smaller than read length")
                except ValueError, v:
                    raise Usage("Argument to -L must be a positive integer.")
            if o in ("-o",):
                if os.path.exists(a):
                    raise Usage("Output file %s already exists" % a)
                else:
                    output = open(a, 'w')
            if o in ("-n",):
                try:
                    n_reads = int(a)
                    if n_reads < 1:
                        raise Usage("Number of reads must be a positive integer.")
                except ValueError, v:
                    raise Usage("Number of reads must be an integer.")
            else:
                raise Usage("Unhandled option: " + o)

        if len(args) != 2:
            raise Usage("generate_reads.py takes exactly two arguments.")

        [fasta, centers] = args

        if not(os.path.exists(fasta)):
            raise Usage("Fasta file %s does not exist." % fasta)
        elif not(os.path.exists(centers)):
            raise Usage("CSV file %s does not exist." % centers)

        genome = read_fasta(fasta)
        with open(centers, 'r') as c:
            peaks = csv.reader(c)
        
        sampler = Sampler(genome, peaks, read_len, frag_len, stdev)
        
        for i in xrange(n_reads):
            output.write(sampler.sample())

        output.close()

        sys.exit(0)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, usage
        return 2
    

if __name__ == '__main__':
    sys.exit(main())
