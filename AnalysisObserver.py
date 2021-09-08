"""
A observer intended to run analysis R scripts during simulation.
"""
import os
import base


class AnalysisObserver(base.Observer):
    """
    A observer that runs R scripts.
    """
    # RELEASES
    VERSION = base.VersionCollection(
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
    VERSION.changed("2.0.4", "Updated documentation and use of markdown in changelog")
    VERSION.changed("2.0.5", "Renamed `LICENSE.txt` to `LICENSE` ")
    VERSION.changed("2.1.0", "Updated runtime environment to R 4.1.1")

    def __init__(self, data, script, output_folder, **keywords):
        super(AnalysisObserver, self).__init__()
        script = os.path.abspath(script)
        if not os.path.isfile(script):
            raise FileNotFoundError('AnalysisObserver script "' + script + '" not found')
        self._componentPath = os.path.dirname(__file__)
        self._wd = os.path.dirname(output_folder)
        # noinspection SpellCheckingInspection
        self._rCall = [os.path.join(self._componentPath, "R-4.1.1", "bin", "x64", "Rscript.exe"), "--vanilla", script]
        for key, value in keywords.items():
            if key != "lock":
                self._rCall.append("--" + key + "=" + value)
        self._rCall.extend([data, output_folder])
        os.makedirs(output_folder, exist_ok=True)
        return

    def experiment_finished(self, detail=None):
        """
        Function that is called when an experiment has finished.
        :param detail: Additional information.
        :return: Nothing.
        """
        base.run_process(self._rCall, self._wd, self.default_observer)
        return

    def input_get_values(self, component_input):
        """
        Function that is called when values are retrieved.
        :param component_input: The input that delivers values.
        :return: Nothing.
        """
        return

    def mc_run_finished(self, detail=None):
        """
        Function that is called when a Monte Carlo run has finished.
        :param detail: Additional information.
        :return: Nothing.
        """
        base.run_process(self._rCall, self._wd, self.default_observer)
        return

    def store_set_values(self, level, store_name, message):
        """
        Function that is called when values are saved in a data store.
        :param level: The level of the message.
        :param store_name: The name of the data store.
        :param message: The message itself.
        :return: Nothing.
        """
        return

    def write_message(self, level, message, detail=None):
        """
        Sends a generic message to the observer.
        :param level: The level of the message.
        :param message: The message itself.
        :param detail: Additional information.
        :return: Nothing.
        """
        return

    def mc_run_started(self, composition):
        """
        Function that is called when a Monte Carlo run starts.
        :param composition: The composition of the Monte Carlo run.
        :return: Nothing.
        """
        return

    def flush(self):
        """
        Flushes the reporter's buffer.
        :return: Nothing.
        """
        return

    def write(self, text):
        """
        Writes a text using the reporter.
        :param text: The text to write.
        :return: Nothing.
        """
        return
