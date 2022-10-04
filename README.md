# D(r)a[r]win(g)

Drawing using Darwinian principles.  
We use the principles of crossover, mutation and survival of the fittest to evolve beautiful images. 

## Painting
There is currently one genetic algorithm available which uses brush strokes to generate a painted version of the target image.
To make sure the algorithm converges fast it is best to not run it on too large images. 
However, to get the most beautiful results, there is a certain sweet spot of brush size to image ratio you could want to hit.  
To reach convergence around that sweet spot you are aiming for you could try changing the image size, or the _min_brush_size_.

## Postprocessing
If pickling was enabled during the run, 
you can always load a pickled specimen again, and redraw the painting at a higher resolution 
using _utils/redraw_painting.py_.
This enables you to first run on a low resolution so that convergence is fast, 
while still achieving a high-resolution end-result. 

## Batch Processing
In _utils/batch_processing.py_ there are some examples on how to run drarwing multiple times with different settings.
The code that is there currently was used to produce the results you see in the gallery.

## Implementing your own Genetic Algorithms
This project includes a small common library of functions and primitives that should give you a nice starting point to create your own genetic algorithms. 
You can also add your own implementation in the _genetic_algorithms_ folder. 
Just pass the filename of your implementation to drarwing as _--algorithm_name_ when invoking it via the commandline. 
You should not have to change the CLI code as long as the file with your custom implementation provides a _get()_ function.
Additional arguments to your algorithm can be specified through _--algorithm_arguments_

## Creating Gifs
After running drarwing you can use a tool like imagemagick to convert the results to a gif.  
On Windows I use: 
```
magick -delay 20 -loop 0 *.png drarwing.gif
```
