"""Copyright 2022 by Artem Ustsov"""

from typing import List

from dataclasses import dataclass, field


@dataclass()
class DownloadParams:
    paths: List[str]
    output_folder: str
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket: str = field(default="ml_project")
    s3_endpoint_url: str = field(default="https://hb.bizmrg.com")
