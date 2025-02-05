import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get the URL parameter from the request
    url = req.params.get('url')
    
    if not url:
        return func.HttpResponse("Missing URL parameter", status_code=400)
    
    try:
        # Fetch content from the external URL
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

        # Read content and determine its length
        content = response.content
        content_length = len(content)

        # Return the response with Content-Length header
        return func.HttpResponse(
            content,
            status_code=200,
            headers={
                "Content-Type": response.headers.get("Content-Type", "application/octet-stream"),
                "Content-Length": str(content_length)  # Ensures compatibility with Azure AI Search
            }
        )

    except requests.exceptions.RequestException as e:
        return func.HttpResponse(f"Error fetching data: {str(e)}", status_code=500)
