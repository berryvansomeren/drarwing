# D(r)a[r]win(g)

Drawing using Darwinian principles.  
We use the principles of reproduction, mutation and survival of the fittest to evolve beautiful images.

## Gallery
Some examples of results. The code for all of these can be found in _mains/batch_processing.py_.

## Evolution of Images
Darwin defined evolution as "descent with modification". 
DNA defines a specimens properties. 
Specimen whose properties better fit their environment produce more offspring. 
Offspring differs from its ancestors through mutations in their DNA.

We can use a similar process to achieve arbitrary goals as long as we modify our definitions of these three rules appropriately. 
In this project "fitness" simply measures how well an image approximates a target image.
The DNA of our image defines what brush strokes to make on a canvas to paint the image. 
Every mutation could add a brush stroke to our image, or change the properties of an already existing brush stroke.

There are currently three different Genetic Algorithms available in this project, 
but it has been set up such that it should be easy to create more variations. 
Because I want to encourage people to modify the python code and not simply invoke existing code, 
there is no CLI available.

Note that in order to get fast feedback on how the algorithm converges,
I have actually used a population size of 1 for two of the currently available algorithms. 
That means that these could also have been written as a for-loop, where it simply accepts or rejects a new brush stroke, based on whether it improves the fitness score. 
While it might sound like a genetic algorithm overcomplicates things in that regard, 
I have found that it enables tremendous freedom in configuration and exploration of these algorithms and variations.

Other tricks I have used to speed up convergence and improve looks are; 
using the differences with the target image to further guide the area of mutation,
using the magnitude of the overall differences to scale modifications,
and using the gradient of the target image to guide the direction of brush strokes. 
However, instead of optimizing perfectly we embrace the random number generator,
and allow it to select suboptimal modifications in order to achieve a more artsy effect. 

This project was inspired by:
- https://github.com/anopara/genetic-drawing
- https://github.com/matteo-ronchetti/Pointillism
