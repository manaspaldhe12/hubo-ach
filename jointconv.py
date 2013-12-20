#!/usr/bin/env python

import sys
import numpy as np
import math

if len(sys.argv) != 4:
    print 'usage: jointconv.py JOINT ENC enc'
    print '   or: jointconv.py JOINT RAD rad'
    print '   or: jointconv.py JOINT DEG deg'
    print
    sys.exit(1)

name = sys.argv[1]
quantity = float(sys.argv[2])
conv = sys.argv[3]

if conv not in ['enc', 'rad', 'deg']:
    print 'bad conversion', conv
    sys.exit(1)

dtype = np.dtype({'names': ['name', 'motNo', 'refEnc', 'drive', 'driven', 'harm', 'enc', 'dir', 'jmc', 'active', 'can', 'numMot', 'kp', 'kd', 'maxPWM', 'zeroed'],
                  'formats': [object, 'f', 'f', 'f', 'f', 'f', 'f', 'f', object, 'f', 'f', 'f', 'f', 'f', 'f', 'f']})


data = np.genfromtxt('/etc/hubo-ach/drc-hubo.joint.table',
                     dtype=dtype)


idx = np.nonzero( data['name'] == name )[0].flatten()
if (len(idx) == 0):
    print 'joint not found:', name

idx = idx[0]
print 'found joint {0} at index {1}'.format(name, idx)

drive = data['drive'][idx]
driven = data['driven'][idx]
harmonic = data['harm'][idx]
pEnc = data['enc'][idx]

print 'drive={0}, driven={1}, harmonic={2}, pEnc={3}'.format(drive, driven, harmonic, pEnc)

if conv == 'enc':
    enc = quantity
    rad = enc * drive / driven / harmonic / pEnc * 2 * np.pi
    print '{0} enc -> {1} rad'.format(enc, rad)
else:
    if conv == 'deg':
        rad = quantity * np.pi / 180.0
    else:
        rad = quantity
    enc = rad * driven * harmonic * pEnc / drive / 2 / np.pi
    print '{0} rad -> {1} enc'.format(rad, enc)









