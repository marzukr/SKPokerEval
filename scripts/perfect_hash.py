#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SKPokerEval
#
# Copyright 2010 Kenneth J. Shackleton
#
# This program gives you software freedom; you can copy, convey, propagate,
# redistribute and/or modify this program under the terms of the GNU General
# Public License (GPL) as published by the Free Software Foundation (FSF),
# either version 3 of the License, or (at your option) any later version of
# the GPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program in a file in the top-level directory called "GPLv3". If
# not, see http://www.gnu.org/licenses/.

# A Czech-Havas-Majewski perfect hash implementation.
# See "Fundamental Study Perfect Hashing" by Czech, Havas, Majewski,
# Theoretical Computer Science 182 (1997) 1-143.
#
# Modified by sorting input so as to always write densest rows first.

from rank import rank

val = [0, 1, 5, 22, 98, 453, 2031, 8698, 22854, 83661, 262349, 636345, 1479181]
keys = set([])
max_key = 0

for i in xrange(1, 13):
    for j in xrange(1, i+1):
        for k in xrange(1, j+1):
            for l in xrange(0, k+1):
                for m in xrange(0, l+1):
                    if not m < i: break
                    for n in xrange(0, m+1):
                        if not n < j: break
                        for p in xrange(0, n+1):
                            if not p < k: break
                            key = val[i] + val[j] + val[k] + val[l] + val[m] +\
                                val[n] + val[p]
                            keys.add(key)
                            max_key = max(max_key, key)

print "Key count is %i." % (len(keys),)
print "Max key is %i." % (max_key,)

side = 128 # Power of 2 to ultimately optimise hash key calculation.
print "Square will be of side %i." % (side,)

square = [[-1]*(512*side) for i in xrange(side)]

offset = [0]*((max_key / side) + 1)
ranks = [-1]*max_key
length = 0

counts = [0]*len(offset)

for k in keys:
    r = k / side
    square[k % side][r] = rank(k)
    counts[r] += 1

sorted_rows = sorted(
    xrange(0, len(offset)),
    key=lambda x: counts[x],
    reverse=True)

for i in xrange(0, len(offset)):
    for j in xrange(0, len(ranks)-side):
        collision = False
        for k in xrange(0, side):
            s = square[k][sorted_rows[i]]
            h = ranks[j+k]
            collision = (s != -1 and h != -1 and s != h)
            if collision: break
        if not collision:
            offset[sorted_rows[i]] = j
            for k in xrange(0, side):
                s = square[k][sorted_rows[i]]
                if s != -1:
                    n = j+k
                    ranks[n] = s
                    length = max(length, n+1)
            print "Offset of row %i is %i (length %i)." % (sorted_rows[i], j, length)
            break

for i in xrange(0, length):
    if ranks[i] == -1: ranks[i] = 0

with open('./ranks_sort_%s' % (side,), 'w') as f:
    f.write("%s\n" % (ranks[0:length],))

with open('./offset_sort_%s' % (side,), 'w') as f:
    f.write("%s\n" % (offset,))

print "Hash table has length %i." % (length,)
