# can choose to just import mesa or to do these and streamline code a little
from mesa import Agent
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


# set up and initialize the agents
class SegAgent(Agent):
    def __init__(self, pos, model, agent_type, wealth):  # agents and their characteristics
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type
        self.similar = 0  # agent-specific measures of neighbor similarity
        self.similar0 = 0
        self.similar1 = 0
        self.neighbors_a = 0  # count of neighbors for each agent (ignore empty squares)
        self.a_pct_similar = 0  # calculate neighbor percents
        self.oldpos=pos
        self.wealth=wealth #create wealth attribute to track the wealth of agent
        self.neighborwealth=0 #create neighborwealth attribute to track the average wealth of neighbors

    # describe what happens in each step for the agents
    # agents check surroundings and count neighbors of the same type and calculate the average wealth of neighbors
    def step(self):
        self.similar = 0  # reset these counters each time step
        self.similar0 = 0
        self.similar1 = 0
        self.neighbors_a = 0
        self.a_pct_similar = 0
        self.neighborwealth=0


        # get neighbors and determine if your intolerance threshold is met
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            self.neighbors_a += 1
            self.neighborwealth+=neighbor.wealth




            if neighbor.type == self.type:
                self.similar += 1

                if self.type == 0:
                    self.similar0 += 1

                elif self.type == 1:
                    self.similar1 += 1

       # wealth gain and loss based on the mean wealth of neighbors
        if self.neighborwealth!=0:
            self.neighborwealth=self.neighborwealth/len(self.model.grid.get_neighbors(self.pos, True))

        if (float(self.wealth)<self.neighborwealth*(1-self.model.intolerance)) & (self.wealth<self.model.totalwealth):
            self.wealth+=self.neighborwealth/100*(self.similar/len(self.model.grid.get_neighbors(self.pos, True)))
        elif float(self.wealth)>self.neighborwealth*(1+self.model.intolerance):
            self.wealth-=self.neighborwealth/100


        # If unhappy, move:
        # this permits different types to have different group thresholds
        if self.type == 0:
            if self.similar < 8 * self.model.intolerance or self.neighborwealth< self.wealth * self.model.intolerance:





                if self.wealth>0:
                    self.oldpos=self.pos

                    newpos=self.model.grid.find_empty()

                    moving_cost=abs(newpos[0]-self.oldpos[0])+abs(newpos[1]-self.oldpos[1]) #use distance as cost

                    #max distance to move based on unhappiness
                    if self.wealth > moving_cost and moving_cost != 0:
                        maxmoving = ((8 - self.similar) / 8 + (self.wealth - self.neighborwealth) / self.wealth) / 2 * 30
                        if moving_cost<maxmoving:

                            self.model.grid.move_agent(self, newpos)
                            self.wealth=self.wealth-moving_cost



            else:
                self.model.happy += 1
                self.model.happy0 += 1
        else:
            if self.similar < 8 * self.model.intolerance or self.neighborwealth < self.wealth * self.model.intolerance:




                if self.wealth > 0:
                    self.oldpos = self.pos

                    newpos = self.model.grid.find_empty()

                    moving_cost = abs(newpos[0] - self.oldpos[0] + newpos[1] - self.oldpos[1])

                    if self.wealth > moving_cost and moving_cost != 0:
                        maxmoving = ((8 - self.similar) / 8 + (self.wealth - self.neighborwealth) / self.wealth) / 2 * 30
                        if moving_cost<maxmoving:
                            self.model.grid.move_agent(self, newpos)



                            self.wealth = self.wealth - moving_cost


            else:
                self.model.happy += 1
                self.model.happy1 += 1


        if self.neighbors_a > 0:
            self.a_pct_similar = round(100 * self.similar / self.neighbors_a, 1)
        else:
            self.a_pct_similar = 0

    # set up the actions available to agents
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)

        self.model.grid.move_agent(self, new_position)

