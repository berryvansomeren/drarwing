# Notes

These notes are primarily meant to summarize approaches fo inspirational projects similar to this one. 

### [4dcu triangles](https://blog.4dcu.be/programming/2020/01/12/Genetic-Art-Algorithm.html):

- sigma term for mutation size. Is determined manually.
- Crossover: For every gene select if getting form mom or dad, other child gets the other option
- survival rate: 0.05 (how many are used as parent)
- n genes = 150
- population size = 200

### [4dcu voronoi](https://blog.4dcu.be/programming/2020/02/10/Genetic-Art-Algorithm-2.html)

- Genes are points with colors that define a voronoi diagram
- crossover like above for triangles
- After converging, 
  randomly remove n points, 
  then duplicate voronoi points
  then evolve again. Because points at the exact same locaton dont affect the image, this allows for potentially more detail, but does not distort the image
- survival rate: 0.025
- n genes = 250
- population size = 250

### [anapora](https://github.com/anopara/genetic-drawing)

- it's not really a GA
  - they just update the best image with one additional brush stroke every iteration
  - there is no crossover between specimen
- does edge detection to determine sampling area
  - applies a huge blur to cover non-edge areas
  - edges are also used to determine size and direction
- separated into stages where every stage has a fixed number of generations
  - blur is updated every stage

### [pointilism](https://github.com/matteo-ronchetti/Pointillism)
- softmax for determining brush size and shape

### Next up:
- Remember that you were fuckign aorudn with replacing HSB with RGB again 
- Use same brushsize estimation as pointillism
- use a palette like pointilism
- check what the scharr image looks like, do you need to porocess it further? larger kernel? erosion? neighborhood summing?
- try ideas with poisson disc sampling
- concurrency?
- dynamic scharr blurring

Note that not all algortihms now return an RGB image when they should!!!