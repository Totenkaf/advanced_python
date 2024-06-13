"""Copyright 2022 by Artem Ustsov"""

from setuptools import find_packages, setup


with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="ml_project",
    packages=find_packages(),
    version="0.1.0",
    description="Example of ml project",
    author="Artem Ustsov (Technopark, ML-21)",
    entry_points={
        "console_scripts": [
            "ml_project_download_data_from_s3 = "
            "ml_project.ml_project_download_data_from_s3:download_data_from_s3_command",
            "ml_project_make_eda = ml_project.make_eda:make_eda_command",
            "ml_project_fit = ml_project.fit_predict_pipeline:fit_pipeline_command",
            "ml_project_predict = ml_project.fit_predict_pipeline:predict_pipeline_command",
        ]
    },
    install_requires=required,
    license="MIT",
)
