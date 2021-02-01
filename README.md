# Neural Style Transfer for Ikomia

This plugin is based on the [PyImageSearch tutorial](https://www.pyimagesearch.com/2018/08/27/neural-style-transfer-with-opencv/) written by Adrian Rosebrock.

It provides ready to use method to render an image with the painted style of a given list of reference images (from famous painter). The model is trained on a closed list of reference pictures, it can't render style from a new reference image dynamically.

### Trained models

ECCV16
- [the_wave.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/the_wave.t7)
- [starry_night.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/starry_night.t7)
- [la_muse.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/la_muse.t7)
- [composition_vii.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/composition_vii.t7)

Instance norm
- [candy.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/candy.t7)
- [la_muse.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/la_muse.t7)
- [mosaic.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/mosaic.t7)
- [feathers.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/feathers.t7)
- [the_scream.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/the_scream.t7)
- [udnie.t7](http://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/udnie.t7)

### How to use it?
Here are the steps:

1. Create Ikomia account for free [here](https://ikomia.com/accounts/signup/) (if you don't have one)
2. Install [Ikomia software](https://ikomia.com/en/download)
3. Launch the software and log in with your credentials
4. Open Ikomia Store and install NeuralStyleTransfer plugin
5. Open your images
6. Add NeuralStyleTransfer algorithm to the workflow
7. Start the workflow and evaluate the prediction

That's it!
