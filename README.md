# PyPlot_orientedmap
The Python package for plotting planar and toroidal maps.

The installation is done first by building some environment. This can be done for example by:
```sh
python3 -m venv $HOME/my_environment
source $HOME/my_environment/bin/activate
```

Then the installation is done in the following way:
```sh
pip3 install git+https://github.com/MathieuDutSik/PyPlot_orientedmap
```
which will compile the C++ binaries of polyhedral and install them.


## Usage

The program is used in the following way for a toric graph:

```python
import pyplot_orientedmap
l_next  =[3,6,9,0,12,15,1,16,14,2,13,17,4,10,8,5,7,11]
l_invers=[1,2,0,4,5,3,7,8,6,10,11,9,13,14,12,16,17,15]
svg_file = "map_4_4_8.svg"
pyplot_orientedmap.draw_svg_file(l_next, l_invers, svg_file)
```
