# pyminder

I use Beeminder in a lot of my Python projects, and I find myself writting the same helper functions multiple times. 
This repository will serve as a place for me to store this functionality and make it accessible to other people.

## Usage

```python
import time
from pyminder.pyminder import Pyminder

pyminder = Pyminder(user='[your username]', token='[your api token]')

goals = pyminder.get_goals()
goal = goals[0]

# Goal objects expose all API data as dynamic properties.
# http://api.beeminder.com/#attributes-2
slug = goal.slug
rate = goal.rate

# Goal objects also implement a handful of helper functions.
# Note: These functions probably contain bugs! Issues & pull requests welcome.
# https://github.com/narthur/pyminder/blob/master/pyminder/goal.py
now = time.time()
sum_ = goal.get_data_sum(now)
needed = goal.get_needed(now)
```

## Links

- [PyPI](https://pypi.org/project/pyminder/)
- [GitHub](https://github.com/narthur/pyminder)

## Development

- Set up a virtual environment in PyCharm so you aren't using the global Python env. This will allow you to avoid
conflicts of dependencies.
- `pip install twine wheel`

## Deployment

- Update version number in `setup.py`
- `python setup.py sdist bdist_wheel`
- Check that expected files are included: `tar tzf dist/pyminder-{ version }.tar.gz`
- `twine check dist/*`
- Test publish: `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
- Publish using PyPi credentials: `twine upload dist/*`

## Information

- [Beeminder API Reference](http://api.beeminder.com/#beeminder-api-reference)
- [How to Publish an Open-Source Python Package to PyPI](https://realpython.com/pypi-publish-python-package/)
- [Building and Distributing Packages with Setuptools](https://setuptools.readthedocs.io/en/latest/setuptools.html#basic-use)
