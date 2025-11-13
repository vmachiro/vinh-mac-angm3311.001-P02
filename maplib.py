import maya.cmds as cmds
import houselib as house

# build a second GUI to be utilized that focuses on the map parameters rather than the house parameters.

class Grid():
    def __init__(self):
        # input most basic parameters to build the grid of houses
        # population of houses since we already have number of houses? roads
        
        population_scale = 1 # this determines how many houses are on each square/grid
        roads = 0 # for now, this just determines whether or not there are roads

    # TODO:
    # (FIRST) define a method that makes the flat plane that the houses sit on
    #   transform the plane to be on level with the houses. or vice versa
    #   for every population_scale, add another subdivision/scale the plane larger? 
    #   OR repeat the loop of creating and populating the plane with houses and shift the duplicate to the side

    # TODO:
    # define a method that populates the houses onto the map using House()
    #   instance a House() object
    #   make. the houses based on set default parameters within the class

    # TODO:
    # define a method that flips the groups of houses to face different directions
    #   can probably reuse the window rotation code
    #   

    # TODO:
    # (LAST) define a method that puts a road on the map around the houses. 
    #   probably just a straight path for minimalization


# POLISH:
# figure out house randomization
# user customizability of the houses comes after roads 
# GUI should call the house generator at some point with a button, so that the user can fine tune how the houses look
