# can choose to just import mesa or to do these and streamline code a little
import mesa
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from agents import SegAgent


# set up the model and initialize the world
class SegModel(Model):
    schedule_types = {
        "Sequential": mesa.time.BaseScheduler,
        "Random": mesa.time.RandomActivation,
        "Simultaneous": mesa.time.SimultaneousActivation,
    }

    height = 16
    width = height
    schedule_type = "Random"
    # adding agents to the world
    def __init__(self, width, height, schedule_type, num_agents, minority_pc, intolerance, inequality):
        self.num_agents = num_agents  # we're allowing these values to be set at each run
        self.minority_pc = minority_pc
        self.intolerance = intolerance

        self.width = width
        self.height = height

        self.grid = SingleGrid(width, height, torus=True)
        #self.schedule = RandomActivation(self)
        self.inequality =inequality #inequality attribute
        self.totalwealth=200 #total social wealth for two agents
        self.schedule_type = schedule_type
        self.schedule = self.schedule_types[self.schedule_type](self)
        # global measures for how agents are doing overall
        self.happy = 0
        self.happy0 = 0
        self.happy1 = 0
        self.similar_g = 0
        self.similar_g0 = 0
        self.similar_g1 = 0
        self.num_agents0 = 0
        self.num_agents1 = 0
        self.neighbors_g = 0
        self.neighbors_g0 = 0
        self.neighbors_g1 = 0
        self.pct_neighbors = 0
        self.pct_neighbors0 = 0
        self.pct_neighbors1 = 0
        self.pct_neighbors_e = 0
        self.pct_neighbors_e0 = 0
        self.pct_neighbors_e1 = 0

        # placing agents at random in the world
        # setting finite number of each agent type
        self.num_agents1 = round(self.num_agents * self.minority_pc)
        self.num_agents0 = self.num_agents - self.num_agents1

        for i in range(self.num_agents):

            if i < self.num_agents1:
                self.agent_type = 1
                self.wealth=self.totalwealth*inequality #assign wealth to agent based on inequality index
            else:
                self.agent_type = 0
                self.wealth = self.totalwealth-self.totalwealth*inequality #assign wealth to agent based on inequality index

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            agent = SegAgent(i, self, self.agent_type, self.wealth)
            self.schedule.add(agent)
            #self.grid.position_agent(agent, (x, y))
            self.grid.place_agent(agent, self.grid.find_empty())

        self.running = True  # need this for batch runner

        # somewhat extensive data collection
        self.datacollector = DataCollector(
            model_reporters={"Pct Happy": lambda m: round(100 * m.happy / m.num_agents, 1),
                             "Pct Happy Group A": lambda m: round(100 * m.happy0 / m.num_agents0, 1),
                             "Pct Happy Group B": lambda m: round(100 * m.happy1 / m.num_agents1, 1),
                             "Avg pct similar neighbors": lambda m: m.pct_neighbors,
                             "Avg pct similar neighbors (A)": lambda m: m.pct_neighbors0,
                             "Avg pct similar neighbors (B)": lambda m: m.pct_neighbors1,
                             "Avg pct similar neighbors (count empty)": lambda m: m.pct_neighbors_e,
                             "Avg pct similar neighbors (A) (count empty)": lambda m: m.pct_neighbors_e0,
                             "Avg pct similar neighbors (B) (count empty)": lambda m: m.pct_neighbors_e1,
                             "Num Agents": lambda m: m.num_agents,
                             "Num Agents (A)": lambda m: m.num_agents0,
                             "Num Agents (B)": lambda m: m.num_agents1,
                             "Pct group B": lambda m: m.minority_pc,
                             "Intolerance": lambda m: m.intolerance},
            
            # Model-level count of happy agents  + subgroup counts
            agent_reporters={"Similar_empty": lambda a: round(100 * a.similar / 8, 1),
                             "Similar_no_empty": lambda a: a.a_pct_similar,
                             "Agent type": lambda a: a.type}
            # Agent-level reporters can allow for individual measures
        )


    # define what happens in one step of the model
    # model stopped when all agents are happy
    def step(self):
        self.happy = 0  # Reset counter of happy agents
        self.happy0 = 0  # Reset counter of happy agents
        self.happy1 = 0  # Reset counter of happy agents
        self.similar_g = 0  # Reset counter of similar agents
        self.similar_g0 = 0  # Reset counter of similar agents
        self.similar_g1 = 0  # Reset counter of similar agents
        self.neighbors_g = 0
        self.neighbors_g0 = 0
        self.neighbors_g1 = 0

        for agent in self.schedule.agents:
            self.neighbors_g += agent.neighbors_a
            self.similar_g += agent.similar

            if agent.type == 0:
                self.neighbors_g0 += agent.neighbors_a
                self.similar_g0 += agent.similar0
            else:
                self.neighbors_g1 += agent.neighbors_a
                self.similar_g1 += agent.similar1

        self.schedule.step()
        self.datacollector.collect(self)

        # calculate % neighbors and include empty cells
        self.pct_neighbors_e = round(100 * self.similar_g / (8 * self.num_agents), 1)
        self.pct_neighbors_e0 = round(100 * self.similar_g0 / (8 * self.num_agents0), 1)
        self.pct_neighbors_e1 = round(100 * self.similar_g1 / (8 * self.num_agents1), 1)

        # solves division by zero issue
        if self.neighbors_g == 0:
            self.pct_neighbors = 0
        else:
            self.pct_neighbors = round(100 * self.similar_g / self.neighbors_g, 1)
            self.pct_neighbors0 = round(100 * self.similar_g0 / self.neighbors_g0, 1)
            self.pct_neighbors1 = round(100 * self.similar_g1 / self.neighbors_g1, 1)

        # stops the model when everyone is happy
        if self.happy == self.schedule.get_agent_count():
            self.running = False


