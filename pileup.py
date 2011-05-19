#!/bin/env python
"""
pileup.py
by Fred Ross, <fred.ross@epfl.ch>
May 19, 2011

Takes a FASTA file of a genome, and a CSV file giving alignments in the form of chromosome,position, and produces a new CSV file of the form chromosome,position,pileup, where pileup is the number of reads whose 5'-most site falls at position on chromosome.
"""
import os
import sys
import csv
import getopt

usage = """Usage: pileup.py [-h] [-o output.txt] fasta align.txt

-h             Print this message and exit
-o output.txt  CSV file to write to (default: stdout)
fasta          Genome to pileup on
align.txt      CSV of alignments (chromosome,position)
"""


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

def pileup(template, alignments):
    p = dict( (chromosome, [0 for x in seq]) 
              for chromosome,seq in template.iteritems())
    for chromosome,pos in alignments:
        pos = int(pos)
        p[chromosome][pos] += 1
    return p

class Usage(Exception):
    def __init__(self,  msg):
        self.msg = msg

def main(argv=None):
    output = sys.stdout
    if argv is None:
        argv = sys.argv[1:]
    try:
        try:
            opts, args = getopt.getopt(argv, "ho:", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                print usage
                sys.exit(0)
            elif o in ("-o",):
                if os.path.exists(a):
                    raise Usage("Output file %s already exists" % a)
                else:
                    output = open(a, 'w')
            else:
                raise Usage("Unhandled option: " + o)

        if len(args) != 2:
            raise Usage("simulate.py takes exactly two arguments.")

        [fasta, alignments] = args

        if not(os.path.exists(fasta)):
            raise Usage("FASTA file %s does not exist" % fasta)
        if not(os.path.exists(alignments)):
            raise Usage("Alignment file %s does not exist" % alignments)

        sequences = read_fasta(fasta)
        output_writer = csv.writer(output)

        with open(alignments) as f:
            r = csv.reader(f)
            p = pileup(sequences, r)
            for chromosome,v in p.iteritems():
                for i,n in enumerate(v):
                    output_writer.writerow((chromosome,i,n))

        output.close()
        sys.exit(0)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, usage
        return 2
    

if __name__ == '__main__':
    sys.exit(main())
