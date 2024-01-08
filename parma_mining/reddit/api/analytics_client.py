"""This module contains the AnalyticsClient class.

AnalyticsClient class which is used to send data to the analytics service.
"""
import json
import os
import urllib.parse

import httpx
from dotenv import load_dotenv

from parma_mining.mining_common.const import HTTP_201, HTTP_404
from parma_mining.reddit.model import CompanyModel


class AnalyticsClient:
    """Client class for sending data to the analytics service."""

    load_dotenv()
    analytics_base = str(os.getenv("ANALYTICS_BASE_URL") or "")

    measurement_url = urllib.parse.urljoin(analytics_base, "/source-measurement")
    feed_raw_url = urllib.parse.urljoin(analytics_base, "/feed-raw-data")

    def send_post_request(self, token: str, data):
        """Send a POST request to the analytics service."""
        api_endpoint = self.measurement_url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = httpx.post(api_endpoint, json=data, headers=headers)

        if response.status_code == HTTP_201:
            return response.json().get("id")
        else:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )

    def register_measurements(
        self, token: str, mapping, parent_id=None, source_module_id=None
    ):
        """Register measurements in the analytics service."""
        result = []

        for field_mapping in mapping["Mappings"]:
            measurement_data = {
                "source_module_id": source_module_id,
                "type": field_mapping["DataType"],
                "measurement_name": field_mapping["MeasurementName"],
            }

            if parent_id is not None:
                measurement_data["parent_measurement_id"] = parent_id

            measurement_data["source_measurement_id"] = self.send_post_request(
                token, measurement_data
            )

            # add the source measurement id to mapping
            field_mapping["source_measurement_id"] = measurement_data[
                "source_measurement_id"
            ]

            if "NestedMappings" in field_mapping:
                nested_measurements = self.register_measurements(
                    token,
                    {"Mappings": field_mapping["NestedMappings"]},
                    parent_id=measurement_data["source_measurement_id"],
                    source_module_id=source_module_id,
                )[0]
                result.extend(nested_measurements)
            result.append(measurement_data)
        return result, mapping

    def feed_raw_data(self, token: str, company: CompanyModel):
        """Send raw data to the analytics service."""
        api_endpoint = self.feed_raw_url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        # make the company model json serializable
        raw_data = json.loads(company.updated_model_dump())
        data = {
            "source_name": str(company.data_source),
            "company_id": str(company.id),
            "raw_data": raw_data,
        }

        response = httpx.post(api_endpoint, json=data, headers=headers)

        if response.status_code == HTTP_201:
            return response.json()
        elif response.status_code == HTTP_404:
            pass
        else:
            raise Exception(
                f"API request failed with status code {response.status_code}"
            )
