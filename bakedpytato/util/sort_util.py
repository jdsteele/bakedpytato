# -*- coding: utf-8 -*-

import re
from itertools import groupby

''' Ned Batchelder's original code:
def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
'''

# The code extended with suitable renamings:
spec_dict = {'Å':'A', 'Ä':'A'}

def spec_order(s):
    return ''.join([spec_dict.get(ch, ch) for ch in s])
    
def trynum(s):
    try:
        return float(s)
    except:
        return spec_order(s)

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ trynum(c) for c in re.split('([0-9]+\.?[0-9]*)', s) ]

def sort_natural(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

def splitondigits(string):
  return [int("".join(chars)) if digits else "".join(chars)
          for digits,chars in groupby(string, str.isdigit)]


"""
asciisorted = sorted(unsorted[:])
alphanumsorted = sorted(unsorted[:], key=splitondigits)
alphanumsorted_2 = unsorted[:]
sort_nicely(alphanumsorted_2)

print
format = "%12s %12s %12s %12s"
print format % tuple("ORIGINAL ASCII ALPHANUM ALPHANUM_2".split())
for orig, asc, al, al_2 in zip(unsorted, asciisorted, alphanumsorted, alphanumsorted_2):
  print format % (orig, asc, al, al_2)

'''   THE OUTPUT:

    ORIGINAL        ASCII     ALPHANUM   ALPHANUM_2
      z7.doc  1.2.3.4.123  1.2.3.4.123  1.2.3.4.123
      z4.doc 11.2.3.4.123  2.2.3.4.123  2.2.3.4.123
     z10.doc    123.1.2.3 11.2.3.4.123 11.2.3.4.123
     z14.doc  2.2.3.4.123    123.1.2.3    123.1.2.3
    z101.doc     Angstrom     Angstrom     Angstrom
     z11.doc    Angstrom2    Angstrom2    Angstrom2
      z8.doc       z1.doc       z1.doc     Ängström
     z12.doc      z10.doc       z2.doc     Ångström
     z13.doc     z100.doc       z3.doc   Ångström12
     z15.doc     z101.doc       z4.doc Ängström12.3
      z1.doc     z102.doc       z5.doc       z1.doc
     z18.doc      z11.doc       z6.doc       z2.doc
     z19.doc      z12.doc       z7.doc       z3.doc
      z2.doc      z13.doc       z8.doc       z4.doc
     z20.doc      z14.doc       z9.doc       z5.doc
      z3.doc      z15.doc      z10.doc       z6.doc
    z100.doc      z16.doc      z11.doc       z7.doc
      z5.doc      z17.doc      z12.doc       z8.doc
     z17.doc      z18.doc      z13.doc       z9.doc
      z6.doc      z19.doc      z14.doc      z10.doc
    z102.doc       z2.doc      z15.doc      z11.doc
     z16.doc      z20.doc      z16.doc      z12.doc
      z9.doc       z3.doc      z17.doc      z13.doc
 1.2.3.4.123       z4.doc      z18.doc      z14.doc
   123.1.2.3       z5.doc      z19.doc      z15.doc
 2.2.3.4.123       z6.doc      z20.doc      z16.doc
11.2.3.4.123       z7.doc     z100.doc      z17.doc
    Ängström       z8.doc     z101.doc      z18.doc
    Ångström       z9.doc     z102.doc      z19.doc
    Angstrom     Ängström     Ängström      z20.doc
Ängström12.3 Ängström12.3 Ängström12.3     z100.doc
  Ångström12     Ångström     Ångström     z101.doc
   Angstrom2   Ångström12   Ångström12     z102.doc

'''
"""
