#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    plot_scenario.py
# @author  Joahannes Costa
# @date    2018-08-10
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import sumolib  # noqa
from sumolib.visualization import helpers

import matplotlib.pyplot as plt

#Codigo para rodar
#python /path/to/sumo-0.25.0/tools/visualization/plot_scenario.py -n archive.net.xml

def main(args=None):
    """The main function; parses options and plots"""
    # ---------- build and read options ----------
    from optparse import OptionParser
    optParser = OptionParser()
    optParser.add_option("-n", "--net", dest="net", metavar="FILE",
                         help="Defines the network to read")
    optParser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                         default=False, help="If set, the script says what it's doing")
    optParser.add_option("-w", "--width", dest="width",
                         type="float", default=20, help="Defines the width of the dots")
    optParser.add_option("-c", "--color", dest="color",
                         default='r', help="Defines the dot color")
    optParser.add_option("--edge-width", dest="defaultWidth",
                         type="float", default=1, help="Defines the edge width")
    optParser.add_option("--edge-color", dest="defaultColor",
                         default='k', help="Defines the edge color")
    # standard plot options
    helpers.addInteractionOptions(optParser)
    helpers.addPlotOptions(optParser)
    # parse
    options, remaining_args = optParser.parse_args(args=args)

    if options.net is None:
        print("Error: a network to load must be given.")
        return 1
    if options.verbose:
        print("Reading network from '%s'" % options.net)
    net = sumolib.net.readNet(options.net)
 
    fig, ax = helpers.openFigure(options)
    ax.set_aspect("equal", None, 'C')
    helpers.plotNet(net, {}, {}, options)

    ax.set_xticklabels('')
    ax.set_yticklabels('')

    fig.patch.set_visible(False)
    ax.axis('off')

    #fig.set_size_inches(4.5, 3.5)  
    #fig.savefig('cenario.eps', bbox_inches = 'tight', pad_inches = 0.05, transparent=True)
    plt.show()


if __name__ == "__main__":
    sys.exit(main(sys.argv))

