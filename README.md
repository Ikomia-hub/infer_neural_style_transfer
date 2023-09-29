<div align="center">
  <img src="https://raw.githubusercontent.com/Ikomia-hub/infer_neural_style_transfer/main/icon/icon.png" alt="Algorithm icon">
  <h1 align="center">infer_neural_style_transfer</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/infer_neural_style_transfer">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/infer_neural_style_transfer">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/infer_neural_style_transfer/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/infer_neural_style_transfer.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

Run Neural Style Transfer algorithm.

![Results](https://raw.githubusercontent.com/Ikomia-hub/infer_neural_style_transfer/main/icon/results.png)

## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow

[Change the sample image URL to fit algorithm purpose]

```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="infer_neural_style_transfer", auto_connect=True)

# Run on your image  
wf.run_on(url="https://cdn.pixabay.com/photo/2017/07/11/14/22/pont-du-gard-2493762_960_720.jpg")

# Display transferred style
display(algo.get_output(1))

# Display result
display(algo.get_output(0))
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).

- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters

- **method** (str, default="instance_norm"): method used to train the model. Must be "eccv16" or "instance_norm".
- **model_name** (str, default="candy"): pre-trained model name.  
Model names available per method:
- eccv16
  - the_wave
  - la_muse
  - composition_vii
  - starry_night
- instance_norm
  - candy
  - mosaic
  - the_scream
  - udnie
  - feathers
  - la_muse
- **backend** (str, default="Default"): backend.
- **target** (str, default="CPU"): target.

***Note***: parameter key and value should be in **string format** when added to the dictionary.


```python
from ikomia.dataprocess.workflow import Workflow
from ikomia.utils.displayIO import display

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="infer_neural_style_transfer", auto_connect=True)

algo.set_parameters({
    "method": "eccv16",
    "model_name": "la_muse"
})

# Run on your image  
wf.run_on(url="https://cdn.pixabay.com/photo/2017/07/11/14/22/pont-du-gard-2493762_960_720.jpg")

# Display transferred style
display(algo.get_output(1))

# Display result
display(algo.get_output(0))

```

## :mag: Explore algorithm outputs

Every algorithm produces specific outputs, yet they can be explored them the same way using the Ikomia API. For a more in-depth understanding of managing algorithm outputs, please refer to the [documentation](https://ikomia-dev.github.io/python-api-documentation/advanced_guide/IO_management.html).

```python
import ikomia
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="infer_neural_style_transfer", auto_connect=True)

# Run on your image  
wf.run_on(url="example_image.png")

# Iterate over outputs
for output in algo.get_outputs()
    # Print information
    print(output)
    # Export it to JSON
    output.to_json()
```
