"""
Script for documenting the code of the AnalysisObserver.
"""
import os
import base.documentation
import AnalysisObserver

root_folder = os.path.abspath(os.path.join(os.path.dirname(base.__file__), ".."))
base.documentation.write_changelog(
    "AnalysisObserver",
    AnalysisObserver.AnalysisObserver.VERSION,
    os.path.join(root_folder, "..", "variant", "AnalysisObserver", "CHANGELOG.md")
)
base.documentation.write_contribution_notes(
    os.path.join(root_folder, "..", "variant", "AnalysisObserver", "CONTRIBUTING.md"))
base.documentation.write_repository_info(
    os.path.join(root_folder, "..", "variant", "AnalysisObserver"),
    os.path.join(root_folder, "..", "variant", "AnalysisObserver", "repository.json"),
    os.path.join(root_folder, "..", "..", "..", "versions.json"),
    "observer"
)
