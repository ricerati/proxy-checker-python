import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='proxy_checker',
    version='0.7',
    packages=['proxy_checker'],
    install_requires=['pycurl'],
    author='ricerati',
    description='Proxy checker in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='proxy checker',
    project_urls={
        'Source Code': 'https://github.com/ricerati/proxy-checker-python'
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ]
)
