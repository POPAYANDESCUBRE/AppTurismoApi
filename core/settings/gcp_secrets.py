import json
import os
from google.cloud import secretmanager
from google.auth.exceptions import DefaultCredentialsError

def get_secrets_from_gcp(project_id="popayan-descubre", secret_id="appturismo-django-secrets", version_id="latest"):
    """
    Fetches the secrets JSON payload from Google Cloud Secret Manager.
    Returns a dictionary of secrets.
    """
    try:
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = client.access_secret_version(request={"name": name})

        # Decode the payload.
        payload = response.payload.data.decode("UTF-8")
        
        # Parse and return as a dictionary
        return json.loads(payload)

    except DefaultCredentialsError:
        print("WARNING: GOOGLE_APPLICATION_CREDENTIALS not found or invalid.")
        print("Please ensure you have authenticated with Google Cloud.")
        print("Falling back to empty secrets dictionary (app may crash).")
        return {}
    except Exception as e:
        print(f"ERROR: Failed to fetch secrets from GCP: {e}")
        return {}
