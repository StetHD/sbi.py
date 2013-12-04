sbi
===

.. image:: https://travis-ci.org/vinta/sbi.py.png?branch=master
    :alt: Build Badge
    :target: https://travis-ci.org/vinta/sbi.py

.. image:: https://coveralls.io/repos/vinta/sbi.py/badge.png?branch=master
    :alt: Coverage Badge
    :target: https://coveralls.io/r/vinta/sbi.py?branch=master

.. image:: https://badge.fury.io/py/sbi.png
    :alt: Version Badge
    :target: http://badge.fury.io/py/sbi

.. image:: https://d2weczhvl823v0.cloudfront.net/vinta/sbi.py/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

Dead simple Python wrapper for `Google Search By Image <http://www.google.com/insidesearch/features/images/searchbyimage.html>`_

Installation
============

.. code-block:: bash

    $ pip install sbi

Usage
=====

.. code-block:: python

    import sbi

    result = sbi.search_by(url='http://vinta.s3.amazonaws.com/godness_k.jpg')

    print(result.best_guess)
    """ output:
    Kiko Mizuhara
    """

    print(result.images)
    """ output:
    [
        {
            'url': 'http://img.hudie.com/forum/201308/04/103414ypoypetbqrtvqpej.jpg',
            'width': '612',
            'height': '612',
        },
        {
            'url': 'http://pic.prepics-cdn.com/pib47864010/23041841.jpeg',
            'width': '612',
            'height': '612',
        },
        {
            'url': 'http://show.ellechina.com/Public/uploads/2013/04/18/516fe30ae9d94_ot.jpg',
            'width': '600',
            'height': '600'
        },
        {
            'url': 'http://cfile1.uf.tistory.com/image/253B004051AAF01236D264',
            'width': '550',
            'height': '551',
        },
        ...
        {
            'url': 'http://media-cache-ec0.pinimg.com/236x/44/48/af/4448af8e35b7ef40dd09acf451770d74.jpg',
            'width': '236',
            'height': '236',
        },
    ]
    """

If you prefer dictionary:

.. code-block:: python

    result_dict = result.to_dict()
