"""
Fine-tuning Skeletons
=====================

In this example we will demonstrate various ways to fine-tune plots with skeletons.

By now, you should already have a basic understanding on how to plot neurons in {{ navis }} (2d vs 3d plots, the various
backends and plotting methods, etc.) - if not, check out the [plotting tutorial](../plot_00_plotting_intro).

We will focus on how to finetune [`plot2d`][navis.plot2d] plots because `matplotlib` is much more flexible than the
[`plot3d`][navis.plot3d] backends when it comes to rendering lines. That said: some of the things we show here will also
work for the other backends (Octarine, Vispy and K3d) - just not all.

"""

# %%
# ## Radii
#
# If your skeletons have radii (i.e. there is a non-empty `radius` column in their `.nodes` SWC table), you can plot them as tubes
# instead of lines using the `radius` parameter. By default, `radius` is set to `True` but will quietly fall back to `False` if
# there is no radius information. Here's an example:

import navis
import matplotlib.pyplot as plt

# Load a neuron
n = navis.example_neurons(1, kind="skeleton")

# Plot as tubes (this is the default)
fig, ax = navis.plot2d(n, view=("x", "-z"), method="2d", radius=True)
plt.tight_layout()

# %%
# Setting `radius=False` will plot skeletons as simple lines. This can be useful if you have many neurons because it is faster.

fig, ax = navis.plot2d(n, view=("x", "-z"), method="2d", radius=False)
plt.tight_layout()

# %%
# ## Line width
#
# You can change the line width of the skeletons using the `linewidth` parameter. The default is `1`.

fig, ax = navis.plot2d(
    n,
    view=("x", "-z"),
    method="2d",
    radius=False,
    linewidth=2,  # default linewidth is 1
)

# %%
# `linewidth` can also be used to scale the size of the tubes when `radius=True`:

fig, ax = navis.plot2d(
    n,
    view=("x", "-z"),
    method="2d",
    radius=True,
    linewidth=2,  # double the tube radii
)

# %%
# ## Line style
#
# When `radius=False`, you can change the line style of the skeletons using the `linestyle` parameter. The default is `"-"` (i.e. a solid line).

fig, ax = navis.plot2d(
    n,
    view=("x", "-z"),
    method="2d",
    radius=False,
    linewidth=2,
    linestyle="--"  # dashed line
)

# %%
# The `radius` and `linewidth` parameters will also work with [`plot3d`][navis.plot3d] but the `linestyle` parameter will not.