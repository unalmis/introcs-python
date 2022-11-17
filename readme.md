# IntroCS Python

This is a repository of programs I developed as I learned python.

## About the code

Here are descriptions of some projects in this repository.

- Cambridge mathematician John Conway's Game of Life. `24`
- A high quality, unit tested, sorted tree implementation. This data structure is not found in the official python libraries. Its API supports more operations than typical implementations. `44`
- Binary search and fast discrete distribution random number generation. `42`
- Rumor propagation at a party. `14`
- Euler totient function and plotting the Fourier spike. `21`
- Computing Ramanujan numbers. `21`
- Computing Fibonacci numbers. `33`

## Installation

If needed, install [miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#).

```sh
git clone https://github.com/unalmis/introcs-python.git
cd introcs-python
conda env create --file environment.yml
conda activate introcs-env
cd introcs-1.1
python setup.py install
python setup.py clean --all
```
