"""
Definition of CLarray and CLsarray

Both are subclasses of numpy.ndarray

Used to store curvelet coefficients
generated by CurveLab
"""

# This software was written by Darren Thomson and Gilles Hennenfent.
# Copyright owned by The University of British Columbia, 2006.  This
# software is distributed and certain rights granted under a License
# Agreement with The University of British Columbia. Please contact
# the authors or the UBC University Industry Liaison Office at
# 604-822-8580 for further information.

import numpy as __n
_CLsarray__n = __n
_CLarray__n = __n


class CLsarray(__n.ndarray):
    """
    Curvelet Scale array

    Returned when one scale is taken from a CLarray

    given a CLsarray cs:

    cs(an) returns the data at this CLsarray's scale
    and the angle an

    cs(an,x) return the value at this CLsarray's scale,
    angle an, and the row x

    cs(an,x,y) return the value at this CLsarray's scale,
    angle an, and location (x,y)

    User should normally never need to create these objects
    """
    def __new__(subtype, data, fdct_op=None, fdct_scale=None, dtype=None, copy=False):
        """
        data - any sequence to be wrapped into the CLarray
        fdct_op - fdct operator object that created this CLsarray (or could have)
        fdct_scale - curvelet scale for this object
        dtype - used to force data type to switch
        copy - used to force data copying on CLarray creation
        """
        if not hasattr(subtype, 'fdct_op'):
            subtype.fdct_op = fdct_op
        if not hasattr(subtype, 'fdct_scale'):
            subtype.fdct_op = fdct_scale

        if isinstance(data, __n.ndarray):
            if not copy and (dtype == data.dtype or dtype is None):
                return data.view(subtype)
            else:
                return data.astype(dtype).view(subtype)

        return __n.array(data).view(subtype)

    def __call__(self, *args):
        i0 = self.fdct_op.getindex((self.fdct_scale, 0, 0, 0))
        if len(args) == 0:
            return self
        elif len(args) == 1:
            ind = self.fdct_op.index(self.fdct_scale, args[0])
            return __n.array(self[ind[0]-i0:ind[1]-i0]).reshape(self.fdct_op.sizes[self.fdct_scale][args[0]])
        elif len(args) == 2:
            ind = self.fdct_op.index(self.fdct_scale, args[0], args[1])
            return __n.array(self[ind[0]-i0:ind[1]-i0])
        elif len(args) == 3:
            return self[self.fdct_op.index(self.fdct_scale, args[0], args[1], args[2])-i0]

    def __array_finalize__(self, obj):
        if hasattr(obj, "fdct_op"):
            self.fdct_op = obj.fdct_op
        if hasattr(obj, "fdct_scale"):
            self.fdct_scale = obj.fdct_op


class CLarray(__n.ndarray):
    """
    Curvelet Array

    returned from a forward curvelet transform

    given a CLarray c:

    c(sc) returns the data at scale sc

    c(sc,an) returns the data at scale sc
    and the angle an

    c(sc,an,x) return the value at scale sc,
    angle an, and the row x

    c(sc,an,x,y) return the value at scale sc,
    angle an, and location (x,y)

    User should normally never need to create these objects
    """
    def __new__(subtype, data, fdct_op=None, dtype=None, copy=False):
        """
        data - any sequence to be wrapped into the CLarray
        fdct_op - fdct operator object that created this CLarray (or could have)
        dtype - used to force data type to switch
        copy - used to force data copying on CLarray creation
        """
        if not hasattr(subtype, 'fdct_op'):
            subtype.fdct_op = fdct_op

        if isinstance(data, __n.ndarray):
            if not copy and (dtype == data.dtype or dtype is None):
                return data.view(subtype)
            else:
                return data.astype(dtype).view(subtype)

        return __n.array(data).view(subtype)

    def __call__(self, *args):
        if len(args) == 0:
            return self
        elif len(args) == 1:
            ind = self.fdct_op.index(args[0])
            x = CLsarray(self[ind[0]:ind[1]], fdct_op=self.fdct_op, fdct_scale=args[0])
            x.fdct_scale = args[0]
            return x
        elif len(args) == 2:
            ind = self.fdct_op.index(args[0], args[1])
            return __n.array(self[ind[0]:ind[1]]).reshape(self.fdct_op.sizes[args[0]][args[1]])
        elif len(args) == 3:
            ind = self.fdct_op.index(args[0], args[1], args[2])
            return __n.array(self[ind[0]:ind[1]])
        elif len(args) == 4:
            return self[self.fdct_op.index(args[0], args[1], args[2], args[3])]

    def __array_finalize__(self, obj):
        if hasattr(obj, "fdct_op"):
            self.fdct_op = obj.fdct_op
