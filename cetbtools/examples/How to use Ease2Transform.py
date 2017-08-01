
# coding: utf-8

# # How to use Ease2Transform
# 
# The Ease2Transform python class contains functions to transform EASE-Grid 2.0 locations between grid (row, col), map (x, y) and geographic (lat, lon) coordinate systems.  
# 
# Ease2Transform is distributed as part of the cetbtools python package available from anaconda.org.  Once you have installed cetbtools in your local python environment, you should be able to import it and get information about the class like this:

# In[1]:

from cetbtools.ease2conv import Ease2Transform


# In[2]:

dir(Ease2Transform)


# In[3]:

help(Ease2Transform)


# ### You can instantiate an Ease2Transform object for an EASE-Grid 2.0 projection like this:

# In[4]:

N25 = Ease2Transform("EASE2_N25km")
print N25.gridname


# ### And then call any of the transformation functions like this:

# ### Find the grid coordinates of the North Pole:

# In[5]:

lat, lon = 90., 0.
row, col = N25.geographic_to_grid(lat, lon)
print ("North pole is at:")
print ("  geog coordinates lat=%.3f, lon=%.3f" % (lat, lon))
print ("  grid coordinates row=%.3f, col=%.3f" % (row, col))


# ### Find the geographic coordinates of the UL corner of grid:

# In[6]:

row, col = -0.5, -0.5
lat, lon = N25.grid_to_geographic(row, col)
print ("UL corner of UL cell is:")
print ("  geog coordinates lat=%.3f, lon=%.3f" % (lat, lon))
print ("  grid coordinates row=%.3f, col=%.3f" % (row, col))

