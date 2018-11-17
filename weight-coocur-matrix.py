# Uses dissect toolkit to import the sparse matrix from sort-cooccur-matrix.
# Applies ppmi weighting and exports the result to ./cooccurence/weighted/
# Note that this file is in python 2, not 3.

import sys
import os
folder = os.path.expandvars('/home/luka/Downloads/dissect-master/src')
if folder not in sys.path:
    sys.path.append(folder)
from composes.semantic_space.space import Space

#pathnames
path = '/home/luka/ThLi/cooccurrence/'

#import matrix
holspace = Space.build(data = path+"spm1.sm",
                       rows = path+"rows1.rows",
                       cols = path+"cols1.cols",
                       format = "sm")

#apply ppmi weighting
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting
holspace = holspace.apply(PpmiWeighting())

#export matrix
from composes.utils import io_utils
io_utils.save(holspace, path+"weighted")
holspace.export(path+"weighted_sm", format = "sm")
