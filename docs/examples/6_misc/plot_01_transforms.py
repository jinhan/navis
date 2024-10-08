"""
Transformations
===============

This tutorial will show you how to transform and mirror neurons.

## Introduction

As of version `0.5.0`, {{ navis }} includes functions that let you transform and mirror spatial data (e.g. neurons).
This new functionality splits into high- and low-level functions. In this tutorial, we will start by exploring
the higher-level functions that most users will use and then take a sneak peak at the low-level functions.

At the moment, navis supports the following transform types:

 - [CMTK](https://www.nitrc.org/projects/cmtk/) warp transforms
 - [Hdf5](https://github.com/saalfeldlab/template-building/wiki/Hdf5-Deformation-fields) deformation fields
 - [Elastix](https://elastix.lumc.nl/) transforms
 - landmark-based thin-plate spline transforms
 - affine transforms


### flybrains

Since {{ navis }} brings the utility but does not ship with any transforms, we have to either generate those ourselves or
get them elsewhere. Here, we will showcase the [flybrains](https://github.com/navis-org/navis-flybrains) library that provides
a number of different transforms directly to {{ navis }}. Setting up and registering your own custom transforms will be
discussed further down.

First, you need to get [flybrains](https://github.com/navis-org/navis-flybrains). Please follow the instructions to install
and download the bridging registrations before you continue.
"""

import flybrains

# %%
# Importing `flybrains` automatically registers the transforms with {{ navis }}. This in turn allows {{ navis }} to plot a
# sequence of bridging transformations to map between any connected template spaces.
#
# ![Flybrain Bridging Graph](https://github.com/navis-org/navis-flybrains/blob/main/_static/bridging_graph.png?raw=true)
#
# In addition to those bridging transforms, `flybrains` also contains mirror registrations (we will cover those later), meta data
# and meshes for the template brains:

# This is the Janelia "hemibrain" template brain
print(flybrains.JRCFIB2018F)

# %%
import navis
import matplotlib.pyplot as plt

# This is the hemibrain neuropil surface mesh
fig, ax = navis.plot2d(flybrains.JRCFIB2018F, view=("x", "-z"))
plt.tight_layout()

# %%
# You can check the registered transforms like so:

navis.transforms.registry.summary()

# !!! note
#     The documentation is built in an environment with a minimal number of transforms registered. If you have installed
#     and imported `flybrains`, you should see a lot more than what is shown above.

# %%
# ## Using ``xform_brain``
#
# For high-level transforming, you will want to use [`navis.xform_brain`][]. This function takes a `source` and `target` argument
# and tries to find a bridging sequence that gets you to where you want. Let's try it out:
#
# !!! info
#     Incidentally, the example neurons that {{ navis }} ships with are from the Janelia hemibrain project and are therefore in
#     `JRCFIB2018raw` space ("raw" means uncalibrated voxel space which is 8x8x8nm for this dataset). We will be using those
#     but there is nothing stopping you from using the {{ navis }} interface with neuPrint (the tutorials on
#     [interfaces](../#interfaces)) to fetch your favourite hemibrain neurons and transform those.

# Load the example hemibrain neurons (JRCFIB2018raw space)
nl = navis.example_neurons()
nl

# %%
fig, ax = navis.plot2d([nl, flybrains.JRCFIB2018Fraw], view=("x", "-z"))
plt.tight_layout()

# %%
# Let's say we want these neurons in `JRC2018F` template space. Before we do the actual transform it's useful to quickly check above
# bridging graph to see what we expect to happen:
#
# ??? info "What is JRC2018F?"
#     `JRC2018F` is a standard brain made from averaging over multiple fly brains. See
#     [Bogovic et al., 2020](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0236495) for details.
#
# Have a look at the bridging graph above: first, we know that we are starting in `JRCFIB2018Fraw` space. From there, it's two
# simple affine transforms to go from voxels to nanometers and from nanometers to micrometers. Once we are in `JRCFIB2018Fum` space, we can use a
# Hdf5 transform generated by the Saalfeld lab to map to `JRC2018F`. Note that the arrows in the bridging graph indicate the transforms'
# forward directions but they can all be inversed to traverse the graph.
#
# Let's give this a shot:

xf = navis.xform_brain(nl, source="JRCFIB2018Fraw", target="JRC2018F")

# %%
# Painless, wasn't it? Let's see if it worked:

# %%
# Plot the transformed neurons and the JRC2018F template brain
fig, ax = navis.plot2d([xf, flybrains.JRC2018F], color="r", view=("x", "-y"))
plt.tight_layout()

# %%
# That worked like a charm! I highly recommend you read through the documentation for [`navis.xform_brain`][] and check out the parameters
# you can use to fine-tune it.
#
#
# ## Using ``mirror_brain``
#
# Another useful type of transform is mirroring using [`navis.mirror_brain`][] to e.g. mirror neurons from the left to the right side of
# a given brain. The way this works is this:
#
# 1. Reflect coordinates about the midpoint of the mirror axis (affine transformation)
# 2. Apply a warping transformation to compensate for e.g. left/right asymmetries
#
# For the first step, we need to know the length of the mirror axis. This is why - similar to having registered transforms - we need to have
# meta data about the template space (i.e. the bounding box) available to {{ navis }}.
#
# The second step is optional. For example, `JRC2018F` and `JRC2018U` are templates generate from averaging multiple fly brains and are
# therefore already mirror symmetrical, meaning we don't need the additional warping transform. `flybrains` does include some mirror transforms
# though: e.g. for `FCWB`, `VNCIS1` or `JFRC2`!
#
# Since our neurons are already in `JRC2018F` space, let's try mirroring them:

mirrored = navis.mirror_brain(xf, template="JRC2018F")

# %%
fig, ax = navis.plot2d(
    [xf, mirrored, flybrains.JRC2018F], color=["r"] * 5 + ["g"] * 5, view=("x", "-y")
)
plt.tight_layout()

# %%
# Perfect! As noted above, this only works if the `template` is registered with {{ navis }} and if it contains info about its bounding box.
# If you only have the bounding box at hand but no template brain, check out the lower level function [`navis.transforms.mirror`][].
#
#
# ## Low-level functions
#
# ### Adding your own transforms
# Let's assume you want to add your own transforms. There are four different transform types:
#
# - [`navis.transforms.affine.AffineTransform`][]
# - [`navis.transforms.cmtk.CMTKtransform`][]
# - [`navis.transforms.h5reg.H5transform`][]
# - [`navis.transforms.thinplate.TPStransform`][]
#
# To show you how to use them, we will create a new thin plate spline transform using [`TPStransform`][navis.transforms.thinplate.TPStransform].
# If you look at the bridging graph again, you might note the `"FAFB14"` template brain: it stands for `"Full Adult Fly Brain"` (the `14` is a
# version number for the alignment). We will use landmarks to generate a mapping between this 14th and the previous 13th iteration.
#
# First we will grab the landmarks from the Saalfeld's lab [elm](https://github.com/saalfeldlab/elm) repository:

import pandas as pd

# These landmarks map betweet FAFB (v14 and v13) and a light level template
# We will use only the v13 and v14 landmarks
landmarks_v14 = pd.read_csv(
    "https://github.com/saalfeldlab/elm/raw/master/lm-em-landmarks_v14.csv", header=None
)
landmarks_v13 = pd.read_csv(
    "https://github.com/saalfeldlab/elm/raw/master/lm-em-landmarks_v13.csv", header=None
)

# Name the columns
landmarks_v14.columns = landmarks_v13.columns = [
    "label",
    "use",
    "lm_x",
    "lm_y",
    "lm_z",
    "fafb_x",
    "fafb_y",
    "fafb_z",
]

landmarks_v13.head()

# %%
# Now we can use those landmarks to generate a thin plate spine transform:

# %%
from navis.transforms.thinplate import TPStransform

tr = TPStransform(
    landmarks_source=landmarks_v14[["fafb_x", "fafb_y", "fafb_z"]].values,
    landmarks_target=landmarks_v13[["fafb_x", "fafb_y", "fafb_z"]].values,
)
# note: navis.transforms.MovingLeastSquaresTransform has similar properties

# %%
# The transform has a method that we can use to transform points but first we need some data in `FAFB14` space:

# Transform our neurons into FAFB 14 space
xf_fafb14 = navis.xform_brain(nl, source="JRCFIB2018Fraw", target="FAFB14")

# %%
# Now let's see if we can use the v14:octicons-arrow-right-24:v13 transform:

# Transform the nodes of the first two neurons
pts_v14 = xf_fafb14[:2].nodes[["x", "y", "z"]].values
pts_v13 = tr.xform(pts_v14)

# %%
# Quick check how the v14 and v13 coordinates compare:

# Original in black, transformed in red
fig, ax = navis.plot2d(pts_v14, scatter_kws=dict(c="k"), view=("x", "-y"))
_ = navis.plot2d(pts_v13, scatter_kws=dict(c="r"), ax=ax, view=("x", "-y"))

# %%
# So that did... something. To be honest, I'm not sure what to expect for the FAFB 14:octicons-arrow-right-24:13 transform but let's assume this is correct and move on.
#
# Next, we will register this new transform with {{ navis }} so that we can use it with higher level functions:

# Register the transform
navis.transforms.registry.register_transform(
    tr, source="FAFB14", target="FAFB13", transform_type="bridging"
)

# %%
# Now that's done we can use `FAFB13` with [`navis.xform_brain`][]:

# Transform our neurons into FAFB 14 space
xf_fafb13 = navis.xform_brain(xf_fafb14, source="FAFB14", target="FAFB13")

# %%
fig, ax = navis.plot2d(xf_fafb14, c='k', view=("x", "-y"))
_ = navis.plot2d(xf_fafb13, c='r', ax=ax)

# %%
# ### Registering Template Brains
#
# For completeness, lets also have a quick look at registering additional template brains.
#
# Template brains are represented in navis as [`navis.transforms.templates.TemplateBrain`][] and there is currently no canonical way of
# constructing them: you can associate as much or as little data with them as you like. However, for them to be useful they should have
# a `name`, a `label` and a `boundingbox` property.
#
# Minimally, you could do something like this:

# Construct template brain from base class
my_brain = navis.transforms.templates.TemplateBrain(
    name="My template brain",
    label="my_brain",
    boundingbox=[[0, 100], [0, 100], [0, 100]],
)

# Register with navis
navis.transforms.registry.register_templatebrain(my_brain)

# Now you can use it with mirror_brain:
import numpy as np

pts = np.array([[10, 10, 10]])
pts_mirrored = navis.mirror_brain(pts, template="my_brain")

# Plot the points
fig, ax = plt.subplots()
ax.scatter(pts[:, 0], pts[:, 1], c="k", alpha=1, s=50, label="Original")
ax.scatter(
    pts_mirrored[:, 0], pts_mirrored[:, 1], c="r", alpha=1, s=50, label="Mirrored"
)
ax.legend()

# %%
# While this is a working solution, it's not very pretty: for example, `my_brain` does have the default docstring and no fancy string
# representation (e.g. for `print(my_brain)`). I highly recommend you take a look at how [flybrains](https://github.com/navis-org/navis-flybrains)
# constructs and packages the templates.
#
# ## Acknowledgments
#
# Much of the transform module is modelled after functions written by Greg Jefferis for the [natverse](http://natverse.org). Likewise,
# [flybrains](https://github.com/navis-org/navis-flybrains) is a port of data collected by Greg Jefferis for `nat.flybrains` and `nat.jrcbrains`.
