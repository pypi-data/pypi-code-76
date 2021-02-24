# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vit_keras']

package_data = \
{'': ['*']}

install_requires = \
['scipy', 'tensorflow-addons', 'validators']

setup_kwargs = {
    'name': 'vit-keras',
    'version': '0.0.13',
    'description': 'Keras implementation of ViT (Vision Transformer)',
    'long_description': "# vit-keras\nThis is a Keras implementation of the models described in [An Image is Worth 16x16 Words:\nTransformes For Image Recognition at Scale](https://arxiv.org/pdf/2010.11929.pdf). It is based on an earlier implementation from [tuvovan](https://github.com/tuvovan/Vision_Transformer_Keras), modified to match the Flax implementation in the [official repository](https://github.com/google-research/vision_transformer).\n\nThe weights here are ported over from the weights provided in the official repository. See `utils.load_weights_numpy` to see how this is done (it's not pretty, but it does the job).\n\n## Usage\nInstall this package using `pip install vit-keras`\n\nYou can use the model out-of-the-box with ImageNet 2012 classes using\nsomething like the following. The weights will be downloaded automatically.\n\n```python\nfrom vit_keras import vit, utils\n\nimage_size = 384\nclasses = utils.get_imagenet_classes()\nmodel = vit.vit_b16(\n    image_size=image_size,\n    activation='sigmoid',\n    pretrained=True,\n    include_top=True,\n    pretrained_top=True\n)\nurl = 'https://upload.wikimedia.org/wikipedia/commons/d/d7/Granny_smith_and_cross_section.jpg'\nimage = utils.read(url, image_size)\nX = vit.preprocess_inputs(image).reshape(1, image_size, image_size, 3)\ny = model.predict(X)\nprint(classes[y[0].argmax()]) # Granny smith\n```\n\nYou can fine-tune using a model loaded as follows.\n\n```python\nimage_size = 224\nmodel = vit.vit_l32(\n    image_size=image_size,\n    activation='sigmoid',\n    pretrained=True,\n    include_top=True,\n    pretrained_top=False,\n    classes=200\n)\n# Train this model on your data as desired.\n```\n\n## Visualizing Attention Maps\nThere's some functionality for plotting attention maps for a given image and model. See example below. I'm not sure I'm doing this correctly (the official repository didn't have example code). Feedback /corrections welcome!\n\n```python\nimport numpy as np\nimport matplotlib.pyplot as plt\nfrom vit_keras import vit, utils, visualize\n\n# Load a model\nimage_size = 384\nclasses = utils.get_imagenet_classes()\nmodel = vit.vit_b16(\n    image_size=image_size,\n    activation='sigmoid',\n    pretrained=True,\n    include_top=True,\n    pretrained_top=True\n)\nclasses = utils.get_imagenet_classes()\n\n# Get an image and compute the attention map\nurl = 'https://upload.wikimedia.org/wikipedia/commons/b/bc/Free%21_%283987584939%29.jpg'\nimage = utils.read(url, image_size)\nattention_map = visualize.attention_map(model=model, image=image)\nprint('Prediction:', classes[\n    model.predict(vit.preprocess_inputs(image)[np.newaxis])[0].argmax()]\n)  # Prediction: Eskimo dog, husky\n\n# Plot results\nfig, (ax1, ax2) = plt.subplots(ncols=2)\nax1.axis('off')\nax2.axis('off')\nax1.set_title('Original')\nax2.set_title('Attention Map')\n_ = ax1.imshow(image)\n_ = ax2.imshow(attention_map)\n```\n\n![example of attention map](https://raw.githubusercontent.com/faustomorales/vit-keras/master/docs/attention_map_example.jpg)\n",
    'author': 'Fausto Morales',
    'author_email': 'faustomorales@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/faustomorales/vit-keras',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
