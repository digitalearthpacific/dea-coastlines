import pytest
import json
from click.testing import CliRunner
from coastlines.raster import generate_rasters_cli
from coastlines.vector import generate_vectors_cli
from coastlines.continental import continental_cli
from coastlines.validation import validation_cli


@pytest.mark.dependency()
def test_generate_rasters_cli():
    runner = CliRunner()
    result = runner.invoke(
        generate_rasters_cli,
        [
            "--config_path",
            "configs/dea_coastlines_config_tests.yaml",
            "--study_area",
            "1",
            "--raster_version",
            "tests",
            "--start_year",
            "1988",
            "--end_year",
            "2021",
            "--buffer",
            "0.0",
        ],
    )
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_generate_rasters_cli"])
def test_generate_vector_cli():
    runner = CliRunner()
    result = runner.invoke(
        generate_vectors_cli,
        [
            "--config_path",
            "configs/dea_coastlines_config_tests.yaml",
            "--study_area",
            "1",
            "--raster_version",
            "tests",
            "--start_year",
            "1988",
            "--end_year",
            "2021",
            "--baseline_year",
            "2021",
        ],
    )
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_generate_vector_cli"])
def test_generate_continental_cli():
    runner = CliRunner()
    result = runner.invoke(
        continental_cli,
        [
            "--vector_version",
            "tests",
            "--shorelines",
            "True",
            "--ratesofchange",
            "True",
            "--hotspots",
            "True",
            "--baseline_year",
            "2021",
        ],
    )
    # assert result.output == '' # for debugging
    assert result.exit_code == 0


@pytest.mark.dependency(depends=["test_generate_continental_cli"])
def test_validation_cli(capsys):
    runner = CliRunner()
    result = runner.invoke(
        validation_cli,
        [
            "--inputs_path",
            "data/validation/interim/wrl_narrabeen",
            "--deacl_path",
            "data/processed/tests/coastlines_tests.gpkg",
            "--prefix",
            "tests",
            "--append_stats",
            "True",
            "--markdown_report",
            "True",
        ],
    )

    # Prepare detailed error information
    error_info = {
        "exit_code": result.exit_code,
        "output": result.output,
        "exception": str(result.exception) if result.exception else None,
    }

    # Convert error_info to a formatted string
    error_details = json.dumps(error_info, indent=2)

    # Use the detailed error information in the assertion message
    assert result.exit_code == 0, f"Command failed. Error details:\n{error_details}"
