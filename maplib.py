import maya.cmds as cmds
import houselib as hs

# build a second GUI to be utilized that focuses on the map parameters rather than the house parameters.

class Grid():
    def __init__(self):
        # input most basic parameters to build the grid of houses
        # population of houses since we already have number of houses? roads
        
        self.population_scale = 1 # this determines how many houses are on each square/grid
        self.roads = 0 # for now, this just determines whether or not there are roads

    # TODO:
    # (FIRST) define a method that makes the flat plane that the houses sit on
    def create_plane(self):
        cmds.plane( p=(1, 1, 1), s=10 )
    #   transform the plane to be on level with the houses. or vice versa
    #   for every population_scale, add another subdivision/scale the plane larger? 
    #   OR repeat the loop of creating and populating the plane with houses and shift the duplicate to the side

    # TODO:
    # define a method that populates the houses onto the map using House()
    def place_house(self):
        #   instance a House() object
        house1 = hs.House()
        # set the variables for default testing
        house1.number_of_houses = 3
        #   build the houses
        house1.build()
        #   make. the houses based on set default parameters within the class

    def rotate_house(self):
        # TODO:
        # define a method that flips the groups of houses to face different directions
        #   can probably reuse the window rotation code
        pass

    def make_road(self):
        # TODO:
        # (LAST) define a method that puts a road on the map around the houses. 
        #   probably just a straight path for minimalization
        pass

    def build(self):
        # make the plane
        self.create_plane()
        # make a list to later use to group the houses with the grid
        grid_list= []
        # loop through the population scale in order to make tons of houses using House()
        for scale_num in range(self.population_scale):
            # make houses
            # transform if needed
            # append house thing to list
            # rotate if necessary
            # (polish) add roads
        # freeze transforms
        pass 


# POLISH:
# figure out house randomization
# user customizability of the houses comes after roads 
# GUI should call the house generator at some point with a button, so that the user can fine tune how the houses look

if __name__ == "__main__":
    pass