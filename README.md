# Push Merge ZKP Simulator and More

This codebase is modified from [Pygame Cards by ScienceGamez](https://github.com/ScienceGamez/pygame_cards), which handles graphics and interaction with the mouse and pygame events. The documentation for Pygame Cards can be found [here](https://pygame-cards.readthedocs.io).

* To run a simulation of the Push Merge ZKP, use the file examples/pushmerge_zkp/main.py.

* To run a simulation of the ZKP for Agent Based ACA with variable rule size, use the file examples/variable_rule_size/main.py.

* To run a simulation of the ZKP for reachability of automata networks on a general graph, use the file examples/graph_adjacency_check/main.py.

Some simulations offer "tutorial mode," in which the identities of any face-down cards are shown. This is not how the actual ZKP would proceed, but it may help viewers understand how the ZKP works.

## Troubleshooting:
* You may need to create a virtual environment to handle dependencies. If so, to install packages, first activate the virtual environment using the following command: source .venv/bin/activate.
* To run the code, you may need to install the Cairo graphics package on your device.

## Additional Information:
For a formal description of these and other protocols, see [here](https://www.cee.org/sites/default/files/rsi/Papers/zhangceline_193939_5453198_Zhang_Celine_Sendova_Final.pdf).

## Mistakes:
* The final shuffle of matrix M should be a pile-shifting shuffle, not a pile-scramble shuffle
* Some of the videos should say "cyclic shift" instead of "shuffle" for some shuffles