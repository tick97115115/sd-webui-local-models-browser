import json
import httpx
import os

def log(res_json: str):

    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the file path for log.txt in the same directory
    file_path = os.path.join(script_directory, "log.json")

    # Write to the file in write mode (overwrites if it exists)
    with open(file_path, "w") as file:
        # formatted_json = json.dumps(res_json, indent=4)
        file.write(res_json)
        print(f"Log file written at: {file_path}")


def main():
    # Define the endpoint and the array of strings
    base_url = "http://127.0.0.1:7860/local-models-browser/api/v1/loras/{name}"
    parameters = ["model1", "model2", "model3"]  # Replace with your strings

    r = httpx.get("http://127.0.0.1:7860/local-models-browser/api/v1/loras/names/")
    parameters: list[str] = r.json()
    # Iterate over the parameters
    for param in parameters:
        while True:
            try:
                # Send a GET request with the current parameter
                url = base_url.format(name=param)
                print(f"Sending GET request to: {url}")
                response = httpx.get(url)

                # Check the status code
                if response.status_code == 200:
                    print(f"Success: Received 200 for parameter '{param}'")
                    break  # Proceed to the next parameter
                else:
                    print(f"Error: Received {response.status_code} for parameter '{param}'")
                    err_msg_str = response.json()['message']
                    
                    log(err_msg_str)  # Log the response JSON
                    input("Press 'Enter' to retry...")  # Wait for user input
            except httpx.RequestError as e:
                print(f"Request error occurred: {e}")
                input("Press 'Enter' to retry...")  # Wait for user input

if __name__ == "__main__":
    main()
