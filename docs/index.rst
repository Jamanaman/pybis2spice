.. pybis2SPICE documentation master file, created by
   sphinx-quickstart on Wed Aug  5 15:11:15 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pybis2SPICE documentation
=========================

The pybis2SPICE project aims to provide support for IBIS files to be used in SPICE simulators using existing components.
It achieves this by translating IBIS model waveform tables and IV tables into behavioural sources and voltage controlled
current sources and connecting them to represent the clamping and PU/PD networks of the buffer. These are then surrounded
by the relevant representative passives such as die and package capacitances. The work to achieve this was completed 
primarily by `Kishan Amratia`_  built upon the ecdtools project by `Erik Moqvist`_ to interpret IBIS input files
(https://github.com/eerimoq/ecdtools.git)

The main repository is hosted at (https://github.com/Jamanaman/pybis2spice.git).

.. _Kishan Amratia: <https://github.com/kamratia1/>
.. _Erik Moqvist: <https://github.com/eerimoq/>

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/modules
   user_guide