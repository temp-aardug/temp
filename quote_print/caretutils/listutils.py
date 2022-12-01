# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Aardug. (Website: www.aardug.nl).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

def chunks(iterable, chunkSize):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(iterable), int(chunkSize)):
        yield iterable[i:i + int(chunkSize)]
