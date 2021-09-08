## Table of Contents
* [About the project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About the project
The `AnalysisObserver` observes Landscape Model simulation runs and runs an R script within an R environment whenever
a Monte Carlo run, or an entire experiment, is finished. The observer does also contain a copy of [
FFmpeg](https://ffmpeg.org) for fast rendering of animations.

### Built with
* Landscape Model core v1.6.2
* [R](https://cran.r-project.org) v4.1.1


## Getting Started
The following section gives instructions on how to make use of the `AnalysisObserver` within your model variant. This
information is intended for model developers.

### Prerequisites
Make sure you are using the most recent version of the Landscape Model core that is compatible with this 
`AnalysisObserver` version. The description here assumes a setup as described in the Landscape Model core `README`.

### Installation
1. Copy the observer to the `model\variant` folder of the Landscape Model.
2. Add the observer to the `<Parts>` section of the `model\variant\experiment.xml` file.
3. Provide an R script that will be used for analysis, preferably under `model\variant`. See [usage](#usage) for details
   on how to prepare the R script for running fom the observer.
4. If necessary, install additional required R packages within the R environment bundled with the `AnalysisObserver`. It
   is also possible to update the entire R version, but in this case the path specified in teh component has probably
   also to be updated.
5. Place an `Observer` block within the `model\variant\experiment.xml` and/or the `model\variant\mc.xml` that configures
   the observer to be run after an experiment and/or a Monte Carlo run has finished. See [usage](#usage) for further
   details.


## Usage
The `AnalysisObserver` starts a vanilla instance of the bundled R instance for execution of a specified `Script`. The
observer receives the parameters specified within the observer configuration as named key-value command line 
arguments of the form `--key=value`. Thereby, automatic conversion of keys to lower-case takes place. The R package 
`optparse` can be used for parsing these command line arguments. This makes the configuration of the observer very 
adaptive as the R script developer can specify the arguments needed for the script. The model developer can provide
these arguments through the model configuration. An exception is the two mandatory parameters `Data` and `Output_folder`
that are passed as unnamed arguments in the given order. An example configuration looks like this:

```xml
<Observer module="AnalysisObserver" class="AnalysisObserver">
    <Script>$(_X3DIR_)/../../variant/RiskAnalysis_Experiment.R</Script>
    <Data>$(_EXP_BASE_DIR_)\$(SimID)\mcs</Data>
    <Output_Folder>$(_EXP_BASE_DIR_)\$(SimID)\analysis</Output_Folder>
    <DsName>PecSoil</DsName>
</Observer>
```
If placed in the `<Observers>` section of the `model\variant\experiment.xml`, a script located in the `model\variant`
folder (script path resolved relative to the `_X3DIR_`, see Landscape Model core `README`) is run after the
experiment has finished. `<Data>` (here a folder) and `<Output_folder>` are passed to the script as unnamed command 
line arguments. Additionally, a named argument `dsname` can be accessed from within the script.

The R scripts can make use of the `xRisk` R package that allows accessing X3df data stores.


## Roadmap
The `AnalysisObserver` is considered stable with no further development planned. We suggest to use `ReportingElements`, 
within compositions or within Jupyter notebooks instead.


## Contributing
Contributions are welcome. Please contact the authors (see [Contact](#contact)).


## License
Distributed under the CC0 License. See `LICENSE` for more information.


## Contact
Thorsten Schad - thorsten.schad@bayer.com
Sascha Bub - sascha.bub.ext@bayer.com


## Acknowledgements
* [Apply function progress bars](https://cran.r-project.org/web/packages/pbapply)
* [data.table](https://cran.r-project.org/web/packages/data.table)
* [Direct Labels](https://cran.r-project.org/web/packages/directlabels)
* [FFmpeg](https://ffmpeg.org)
* [ggplot2](https://cran.r-project.org/web/packages/ggplot2)
* [h5](https://cran.r-project.org/web/packages/h5)
* [matrixStats](https://cran.r-project.org/web/packages/matrxistats)
* [openxlsx](https://cran.r-project.org/web/packages/openxlsx)
* [optparse](https://cran.r-project.org/web/packages/optparse)
* [R GDAL bindings](https://cran.r-project.org/web/packages/rgdal)
* [raster](https://cran.r-project.org/web/packages/raster)
