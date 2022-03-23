Installation
============

First, clone the repository.

.. code-block:: sh

   git clone https://github.com/phuang1024/pianoray
   cd pianoray

Requirements
------------

- Python 3.8 or later
- Java

Driver
------

.. code-block:: sh

   make driver
   make install

The driver will be installed as a Python package and can be invoked with
``pianoray``

Kernels
-------

.. code-block:: sh

   make kernels

The kernels will be built to ``build/kernels``. Pass this path to the driver
when using it.
