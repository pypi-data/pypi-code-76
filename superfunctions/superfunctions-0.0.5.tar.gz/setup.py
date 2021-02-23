from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'Metafunctions with less repetition'
LONG_DESCRIPTION = '''

#Warning: Package under development... tons of side effects. Don't rely on it yet!

Metafunctions is an excellent package that allows you to compose functions into metafunctions using a pipe. 

Instead of writing:

```
result = step3(step2(step1(data)))

#or
result_1 = step1(data)
result_2 = step2(result_1)
result_3 = step3(result_2)
```

You instead write:

```
pipeline = step1 | step2 | step3
result = pipeline(data)
```

Here's another example:
```
# load, parse, clean, validate, and format are functions
preprocess = load | parse | clean | validate | format

# preprocess is now a MetaFunction, and can be reused
clean_data1 = preprocess('path/to/data/file')
clean_data2 = preprocess('path/to/different/file')

# Preprocess can be included in larger pipelines
pipeline = preprocess | step1 | step2 | step3
```

"Then why are you making a new package?"

The problem is in the repetition:

You have to do this:
```
from metafunctions import node

@node
def get_name(prompt):
    return input(prompt)

@node
def say_hello(name):
    return 'Hello {}!'.format(name)
```

And then do this:
```
greet = get_name | say_hello
```

Why use the word "@node" over every function? what if I have a big class,
or if I'm importing functions from other modules? 

Do I have to go and decorate every single function in that module to use this syntax?

No!!111!!1 

Unacceptable!

we're developers! We COMPRESS cycles of work, not EXPAND them... 

With superfunctions, all you have to do is:

```
from superfunctions import decorate_all_modules
decorate_all_modules()
```
Make sure this is at the end of all your imports. 

And you're done! That's it!

Wanna use functions from other modules? Piece of cake.

```
import numpy as np
from superfunctions import decorate_all_modules
decorate_all_modules()

g = np.random.rand | np.squeeze | np.sum | print
g(2,3)
```

Wanna use functions from files in the same directory/local modules?

`greetsomeone.py`
```
def get_name(name):
    return name


def say_hello(name):
    return 'Hello {}!'.format(name)
```

And importing from your main file:

```
from greetsomeone import *
from superfunctions import decorate_all_modules
decorate_all_modules()

greet = get_name | say_hello | print
```

BUT it doesn't yet work with all functions.

This is still alpha, and will break a lot and also give you errors you cannot comprehend or even debug!



What does it do?

It does something dangerous...

It decorates ALL functions in all imported modules with "@node" from metafunctions, 
and decorates all methods in all classes in all imported modules,
and decorates all functions and methods in your current file.

Why is this dangerous?

Because this code hasn't been tested yet, we really have no idea
of the side effects. 

Why?

Because I'm still a beginner developer, and I don't know how to write
tests yet. 

Want to help me enhance it, test it, maintain it?
Contact me at ___

Like the package?
Make me less broke by sponsoring me on Github...


Psst... if I had it my way I'd want it to get even closer to english like this:
```
find_first_word_in_titles = get_first_word get_titles parse_html get_html
```
where we remove the pipe! 

But I don't know how to implement this... oh well.

'''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="superfunctions", 
        version=VERSION,
        author="Youssef",
        author_email="youssef.avx@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=['metafunctions', 'collections', 
        'dis', 'inspect'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

