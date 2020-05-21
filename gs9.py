#!/usr/bin/env python

import click

from matplotlib import cm

from glue.config import colormaps
from glue.app.qt.application import GlueApplication
from glue.viewers.image.qt import ImageViewer
from glue.viewers.image.state import ImageLayerState

from glue.main import load_plugins

@click.command()
@click.argument('data')
@click.option('--vmin', type=float)
@click.option('--vmax', type=float)
@click.option('--percentile', type=float)
@click.option('--stretch')
@click.option('--cmap')
def gs9(data, vmin, vmax, percentile, stretch, cmap):

    load_plugins()

    if cmap is not None:
        for cmap_name, cmap_obj in colormaps.members:
            if cmap == cmap_name:
                cmap = cmap_obj
                break
        else:
            colormaps.add(cmap, cm.get_cmap(cmap))
            cmap = cm.get_cmap(cmap)

    ga = GlueApplication()
    d = ga.load_data(data)

    image = ga.new_data_viewer(ImageViewer)
    image.add_data(d)

    layer_state = image.state.layers[0]

    if vmin is not None:
        layer_state.v_min = vmin

    if vmax is not None:
        layer_state.v_min = vmax

    if percentile is not None:
        choices = ImageLayerState.percentile.get_choices(layer_state)
        for choice in choices:
            if percentile == choice:
                percentile = choice
                break
        layer_state.percentile = percentile

    if stretch is not None:
        layer_state.stretch = stretch

    if cmap is not None:
        layer_state.cmap = cmap

    image.viewer_size = (600, 600)

    ga.gather_current_tab()
    ga.start(maximized=False, position=(100, 100), size=(1024, 768))


if __name__ == "__main__":
    gs9()
