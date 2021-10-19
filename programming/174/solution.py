#!/usr/bin/python

with open("data.dat") as fp:
  count = 0
  for line in fp.readlines():
    if line.count('0') % 3 == 0 or line.count('1') % 2 == 0:
      count += 1

  print count
