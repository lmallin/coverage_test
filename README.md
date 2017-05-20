# Gene Coverage Report 

## Aim

The coverage_report.py script takes a sambamba file and generates a pdf report that lists any genes that have less than 100% coverage at 30x. 


## Installation

The script can be run using conda or python virtual environments.

```
cd coverage_test
```

* **Conda:**

Create the conda environment

```
conda env create -f environment.yml 
```

Activate the conda environment
```
source activate coverage_env
```

* **Python virtual environment:**

Activate the python virtual environment
```
source python_venv/bin/activate
```

Dependencies are listed in [requirements.txt](https://github.com/lmallin/coverage_test/python_venv/requirements.txt)

## Generating a report

The coverage_report.py script takes at least one argument to specify the input file.  The output file location can also be specified but will be write to ```coverage_report.pdf``` as default.

```
python coverage_report.py -i [input_file] -o [output_file]
```

## Author
* **Lucy Mallin**

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/lmallin/coverage_test/LICENSE.md) file for details

