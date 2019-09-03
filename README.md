# pyminder

I use Beeminder in a lot of my Python projects, and I find myself writting the same helper functions multiple times. 
This repository will serve as a place for me to store this functionality and make it accessible to other people.

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
