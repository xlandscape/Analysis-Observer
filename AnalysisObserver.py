"""An observer intended to run analysis R scripts during simulation."""
import os
import base


class AnalysisObserver(base.Observer):
    """An observer that runs R scripts."""
    # RELEASES
    VERSION = base.VersionCollection(
        base.VersionInfo("2.1.3", "2021-10-15"),
        base.VersionInfo("2.1.2", "2021-10-12"),
        base.VersionInfo("2.1.1", "2021-10-11"),
        base.VersionInfo("2.1.0", "2021-09-08"),
        base.VersionInfo("2.0.5", "2021-08-05"),
        base.VersionInfo("2.0.4", "2021-06-25"),
        base.VersionInfo("2.0.3", "2021-06-18"),
        base.VersionInfo("2.0.2", "2020-12-07"),
        base.VersionInfo("2.0.1", "2020-12-03"),
        base.VersionInfo("2.0.0", "2020-10-22"),
        base.VersionInfo("1.3.24", "2020-04-02"),
        base.VersionInfo("1.3.13", "2020-02-07"),
        base.VersionInfo("1.2.38", None),
        base.VersionInfo("1.2.36", None),
        base.VersionInfo("1.2.35", None),
        base.VersionInfo("1.2.33", None),
        base.VersionInfo("1.2.12", None),
        base.VersionInfo("1.2.10", None),
        base.VersionInfo("1.2.6", None),
        base.VersionInfo("1.2.2", None),
        base.VersionInfo("1.2.1", None),
        base.VersionInfo("1.1.6", None),
        base.VersionInfo("1.1.3", None),
        base.VersionInfo("1.1.2", None),
        base.VersionInfo("1.1.1", None)
    )

    # CHANGELOG
    VERSION.added("1.1.1", "`observer.AnalysisObserver`")
    VERSION.fixed("1.1.2", "`observer.AnalysisObserver` box-plot labels in `RiskAnalysis_Experiment_PEC` ")
    VERSION.fixed("1.1.3", "`observer.AnalysisObserver` spray-drift/run-off co-occurrence only if both data set exist")
    VERSION.changed("1.1.3", "`observer.AnalysisObserver` visualization threshold defined by median value")
    VERSION.changed("1.1.6", "`observer.AnalysisObserver` info worksheet prepended to Excel worksheet outputs")
    VERSION.changed("1.2.1", "`observer.AnalysisObserver` scripts now use option parser for passing parameters")
    VERSION.changed("1.2.1", "`observer.AnalysisObserver` scripts can now analyse data sets other than PEC soil")
    VERSION.changed("1.2.1", "`observer.AnalysisObserver` scripts modularized")
    VERSION.changed("1.2.2", "`observer.AnalysisObserver` do not pass lock keyword to R in `AnalysisObserver` ")
    VERSION.fixed("1.2.6", "`observer.AnalysisObserver` R functions for multiple habitat types")
    VERSION.fixed("1.2.10", "Geo-raster orientations in class `observer.AnalysisObserver` ")
    VERSION.added("1.2.12", "`observer.AnalysisObserver.mc_run_started()` ")
    VERSION.changed("1.2.33", "`observer.AnalysisObserver` no longer requires scripts to be in observer directory")
    VERSION.changed("1.2.33", "Scripts in class `observer.AnalysisObserver` directory removed")
    VERSION.changed("1.2.35", "Update of `observer.AnalysisObserver` `XRisk` package to v0.0.0.9003")
    VERSION.changed("1.2.36", "Removed generic R functions from class `observer.AnalysisObserver` ")
    VERSION.changed("1.2.38", "Update of `observer.AnalysisObserver` `XRisk` package to v0.0.0.9004")
    VERSION.changed("1.3.13", "`observer.AnalysisObserver` no longer throws error if output directory exists")
    VERSION.added("1.3.24", "`observer.AnalysisObserver`.flush() and observer.AnalysisObserver.write()")
    VERSION.changed("1.3.24", "`observer.AnalysisObserver` uses base function to call observer module")
    VERSION.changed("2.0.0", "First independent release")
    VERSION.added("2.0.1", "Changelog and release history")
    VERSION.added("2.0.1", "`README`, `LICENSE`, `CONTRIBUTING` ")
    VERSION.changed("2.0.2", "Line separators in `LICENSE` ")
    VERSION.changed("2.0.2", "Changelog and `README` modified")
    VERSION.changed("2.0.3", "Updated `data.table` package")
    VERSION.changed("2.0.4", "Updated the documentation and started using markdown in changelog")
    VERSION.changed("2.0.5", "Renamed `LICENSE.txt` to `LICENSE` ")
    VERSION.changed("2.1.0", "Updated runtime environment to R 4.1.1")
    VERSION.changed("2.1.1", "Replaced legacy format strings by f-strings")
    VERSION.changed("2.1.2", "Switched to Google docstring style")
    VERSION.fixed("2.1.3", "Set R module library path")

    def __init__(self, data, script, output_folder, **keywords):
        """
        Initializes an AnalysisObserver.

        Args:
            data: A reference to the input data to be analyzed.
            script: The file path of the R script run by the AnalysisObserver.
            output_folder: The folder where outputs of the analysis script should be written to.
            **keywords: Additional, script-specific arguments for the analysis.
        """
        super(AnalysisObserver, self).__init__()
        script = os.path.abspath(script)
        if not os.path.isfile(script):
            raise FileNotFoundError(f"AnalysisObserver script '{script}' not found")
        self._componentPath = os.path.dirname(__file__)
        self._wd = os.path.dirname(output_folder)
        # noinspection SpellCheckingInspection
        self._rCall = [os.path.join(self._componentPath, "R-4.1.1", "bin", "x64", "Rscript.exe"), "--vanilla", script]
        for key, value in keywords.items():
            if key != "lock":
                self._rCall.append(f"--{key}={value}")
        self._rCall.extend([data, output_folder])
        os.makedirs(output_folder, exist_ok=True)
        self._env = {"R_LIBS_USER": os.path.join(self._componentPath, "R-4.1.1", "library")}

    def experiment_finished(self, detail=None):
        """
        Reacts when an experiment is completed.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        base.run_process(self._rCall, self._wd, self.default_observer, self._env)

    def input_get_values(self, component_input):
        """
        Reacts when values are requested from a component input.

        Args:
            component_input: The input being requested.

        Returns:
            Nothing.
        """

    def mc_run_finished(self, detail=None):
        """
        Reacts when a Monte Carlo run is finished.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        base.run_process(self._rCall, self._wd, self.default_observer, self._env)
