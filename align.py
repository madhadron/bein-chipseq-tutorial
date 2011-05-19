#!/bin/env python
"""
align.py
by Fred Ross, <fred.ross@epfl.ch>
May 19, 2011

Takes a FASTA file of the genome and a file of reads, one per line, and prints a CSV file giving all perfect matches of the reads to the genome.
"""
import os
import csv
import sys
import getopt

usage = """Usage: align.py [-h] [-o output.txt] template.fast reads.txt

-h              Print this message and exit
-o output.txt   Write results to output.txt (default: stdout)
template.fasta  Genome to align to
reads.txt       Sequences to align to the genome
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

def find_all(template, search):
    p = template.find(search)
    if p == -1:
        return []
    else:
        l = [q+p+1 for q in find_all(template[p+1:], search)]
        l.append(p)
        return l

def align_read(template, read):
    alignments = []
    for chromosome, seq in template.iteritems():
        alignments.extend([(chromosome, pos) for pos in find_all(seq, read)])
    return alignments

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
            raise Usage("align.py takes exactly two arguments.")

        [template, reads] = args

        if not(os.path.exists(template)):
            raise Usage("FASTA file %s does not exist" % template)
        if not(os.path.exists(reads)):
            raise Usage("Reads file %s does not exist" % reads)

        sequences = read_fasta(template)
        output_writer = csv.writer(output)
        with open(reads) as reads:
            for r in reads:
                r = chomp(r)
                for a in align_read(sequences, r):
                    output_writer.writerow(a)
        output.close()

        sys.exit(0)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, usage
        return 2
    

if __name__ == '__main__':
    sys.exit(main())
