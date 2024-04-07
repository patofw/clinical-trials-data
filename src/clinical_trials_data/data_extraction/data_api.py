import subprocess
import json


def execute_curl_and_save_response(
        curl_command: str, filename: str, return_data: bool = False
) -> dict | None:
    """Runs a CURL Get command and returns a response.
    For the clinical trials GOV API, this response should
    be set as JSON.

    Args:
        curl_command (str): curl command string
        filename (str): Saving Path.
        return_data (bool, optional): If true, data is returned as a Python dict.
        Defaults to False.

    Returns:
        dict | None: Dictionary of the response
    """
    # Execute the curl command and capture its output
    try:
        print("Calling CTG-API...")
        output = subprocess.check_output(curl_command, shell=True)
        # Decode bytes to string
        output = output.decode('utf-8')

        # Parse JSON response
        data = json.loads(output)

        # Save JSON data to a file
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        if return_data:
            return data
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute curl command: {e}")


if __name__ == "__main__":
    curl_command = '''curl -X GET "https://clinicaltrials.gov/api/v2/studies?format=json&markupFormat=markdown&filter.overallStatus=COMPLETED&pageSize=20" -H "accept: application/json"'''
    filename = "./data/raw/ctg-studies.json"
    execute_curl_and_save_response(curl_command, filename)
