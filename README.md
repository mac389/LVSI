 LVSI
=====
 This repository contains the Python code and supporting data to replicate all figures in Tran et al. (2015). 

Quickstart
=====

#####Clone the repository: 

      git clone https://github.com/mac389/LVSI
      cd LVSI 
      ./configure


#####Generate Figure X:

     make-figure-X

Troubleshoooting. If that fails, you can 

######Fix the code

     chmod +x ./make-figure-X.sh
     export PATH=$PATH:$PWD

######Execute the module corresponding to the figure manually:

     python figure-X.py

##### E-mail mac389@gmail.com

Dependencies
=====

- Python (built on 2.7)
- NumPy
- Matplotlib
- LaTeX 