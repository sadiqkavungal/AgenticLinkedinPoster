import requests
import logging
from typing import Any, Dict
from config import Config

logger = logging.getLogger(__name__)

def post_to_linkedin(content: str) -> Dict[str, Any]:
    """
    Posts a given content string to LinkedIn using the user's access token.
    Returns the JSON response from LinkedIn's API.
    """
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {Config.LINKEDIN_ACCESS_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    payload = {
        "author": f"urn:li:person:{Config.LINKEDIN_USER_ID}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code not in [200, 201]:
        # Attempt to parse LinkedIn API error
        try:
            error_message = response.json()
        except Exception as e:
            error_message = {"error": str(e), "raw_response": response.text}
        
        logger.error("LinkedIn API Error: %s", error_message)

        # If the message indicates an exceeded limit, try reposting shorter content
        if response.status_code == 400 and "exceeded the maximum allowed" in str(error_message):
            logger.warning("Post is too long, attempting to shorten content...")
            shorter_content = content[:Config.LINKEDIN_SAFE_LIMIT] + "\n🔗 [More news here]"
            return post_to_linkedin(shorter_content)
        
        # Return error details 
        return error_message

    return response.json()
