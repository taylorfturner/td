Installation
============

Github
******
.. code-block:: bash

    git clone https://github.com/taylorfturner/td.git
    cd td
    conda create -n td python=3.8
    conda activate td
    pip install -e .


Unit Tests
**********
Unit testing results are written in HTML files to `htmlcov/`. 
Open in preferred browser for futher analysis of "line-level"
coverage and missing lines.

.. code-block:: bash

    pytest --cov=td/ --cov-report html


Sphinx Documentation 
********************

.. code-block:: bash

    cd docs 
    make html    


PyPi
****
Not currently supported and no plans to make publicly available at this in this format.

Conda Forge
***********
Not currently supported and no plans to make publicly available at this in this format.
