# Zheng's Version of Schelling Segregation Model


## Summary

Zheng's version adapts the Schelling segregation model to reflect more about racial segregation, demonstrating how econnomic inequality leads to isolated racial communities. The model consists of agents on a square grid, where each grid cell can contain at most one agent. Agents come in two colors: green and blue. They are happy if a certain number of their eight possible neighbors are of the same color and have the average wealth similar to or higher than them, and unhappy otherwise. Unhappy agents will pick a random empty cell to move to each step with cost, until they are happy. The model keeps running until there are no unhappy agents.

By default, the proportion of similar neighbors and the maximum income gap the agents need to be happy is set to 3/8. That means the agents would be perfectly happy with a majority of their neighbors being of a different color and the neighbors are less wealthy than them(e.g. a Blue agent would be happy with five Green neighbors and three Blue ones and their average wealth is not considerably lower). Despite this, the model consistently leads to a high degree of segregation, with most agents ending up with no neighbors of a different color and poor agents are isolated.

This model also offers three different update scheme to choose.

## Installation

To install the dependencies use pip and the requirements.txt in this directory. e.g.

```
    $ pip install -r requirements.txt
```

## How to Run

To run the model interactively, run ``mesa runserver`` in this directory. e.g.

```
    $ mesa runserver
```

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run.

To view and run some example model analyses, launch the IPython Notebook and open ``analysis.ipynb``. Visualizing the analysis also requires [matplotlib](http://matplotlib.org/).

## How to Run without the GUI

To run the model with the grid displayed as an ASCII text, run `python run_ascii.py` in this directory.

## Files

* ``run.py``: Launches a model visualization server.
* ``model.py``: Contains the overall model class.
* ``agents.py``: Contains the agent class.
* ``server.py``: Defines classes for visualizing the model in the browser via Mesa's modular server, and instantiates a visualization server.


## Further Reading

Schelling's original paper describing the model:

[Schelling, Thomas C. Dynamic Models of Segregation. Journal of Mathematical Sociology. 1971, Vol. 1, pp 143-186.](https://www.stat.berkeley.edu/~aldous/157/Papers/Schelling_Seg_Models.pdf)

An interactive, browser-based explanation and implementation:

[Parable of the Polygons](http://ncase.me/polygons/), by Vi Hart and Nicky Case.
