import mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import SegModel



# define and set up agent visualization
#shalower color and smaller size as wealth decreases
def schelling_draw(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}
    wealth = agent.model.totalwealth/2
    if agent.type == 0:


        if agent.wealth >= wealth*9/10:
            portrayal["Color"] = "DarkGreen"
        elif (agent.wealth < wealth*9/10) & (agent.wealth >= wealth*6/10):
            portrayal["Color"] = "Green"
        elif (agent.wealth < wealth*6/10) & (agent.wealth >= wealth*3/10):
            portrayal["Color"] = "LimeGreen"
        elif (agent.wealth < wealth*3/10) & (agent.wealth >= wealth*1/10):
            portrayal["Color"] = "Lime"
        else:

            portrayal["Color"] = "MediumSpringGreen"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2




    elif agent.type == 1:


        if agent.wealth >= wealth * 9 / 10:
            portrayal["Color"] = "DarkBlue"
        elif (agent.wealth < wealth * 9 / 10) & (agent.wealth >= wealth * 6 / 10):
            portrayal["Color"] = "MediumBlue"
        elif (agent.wealth < wealth * 6 / 10) & (agent.wealth >= wealth * 3 / 10):
            portrayal["Color"] = "Blue"
        elif (agent.wealth < wealth * 3 / 10) & (agent.wealth >= wealth * 1 / 10):
            portrayal["Color"] = "RoyalBlue"
        else:

            portrayal["Color"] = "CornFlowerBlue"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2


    return portrayal


# text elements we're calling
# these next portions allow for the values
# to appear in the gui for the model
class HappyElement(TextElement):

    def render(self, model):
        return "% Happy agents: " + str(round(
            (model.happy / model.num_agents) * 100, 1)) + "%"


class SimilarElement(TextElement):

    def render(self, model):
        return "Avg. % similar neighbors: " + str(model.pct_neighbors) + "%"


class SimilarElement_g(TextElement):

    def render(self, model):
        return "Groups avg. % similar neighbors: (A) " + str(model.pct_neighbors0) + "%" + " (B) " + str(
            model.pct_neighbors1) + "%"




# set up how and what we're calling for the gui
# canvas itself
canvas_element = CanvasGrid(schelling_draw, SegModel.height, SegModel.width, 500, 500)

# text elements
happy_element = HappyElement()
similar_element = SimilarElement()
similar_element_g = SimilarElement_g()

# various charts / reporting options
happy_chart = ChartModule([{"Label": "Pct Happy", "Color": "Black"}])
happy_chart0 = ChartModule([{"Label": "Pct Happy Group A", "Color": "Green"}])
happy_chart1 = ChartModule([{"Label": "Pct Happy Group B", "Color": "Blue"}])


# set up how the visualization will look
model_params = {
    "height": SegModel.height,
    "width": SegModel.width,
    "num_agents": UserSettableParameter('slider', "Number Agents", 
                                      int(0.8 * SegModel.height ** 2), 10, 
                                      SegModel.height * SegModel.width, 10),
    "minority_pc": UserSettableParameter('slider', "% group B", 0.35, 0.00, 1.0, 0.05),
    "intolerance": UserSettableParameter('slider', "Intolerance: (Desired % of matching neighbors) ",
                                          0.375, 0, 1, 0.125),

    "inequality": UserSettableParameter('slider', "inequality",
                                          0.5, 0, 1, 0.05),

    "schedule_type": mesa.visualization.Choice(
        "Scheduler type",
        value="Random",
        choices=list(SegModel.schedule_types.keys()),
    ),
}

# this is where we call the different elements we're going to be visualizing
# it includes the model, the graph/grid/world, and our various charts
# it also features a name for the model and our relevant parameter values
server = ModularServer(
    SegModel,
    [canvas_element, happy_element,
     similar_element, similar_element_g,
     happy_chart, happy_chart0, happy_chart1],
    "Schelling's Segregation Model",
    model_params
)
