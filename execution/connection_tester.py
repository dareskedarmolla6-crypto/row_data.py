import os
import requests
from dotenv import load_dotenv
from requests.exceptions import (
    Timeout,
    ConnectionError,
    HTTPError,
    RequestException
)

# ==========================================
# Load Environment Variables
# ==========================================
load_dotenv()


def test_api_connection():
    """
    Exchange API Connection Tester
    (Used to verify connectivity before trade execution)
    """

    # Load secrets from .env
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    base_url = os.getenv("BASE_URL")

    # ==============================
    # Validate Environment Variables
    # ==============================
    if not api_key:
        print("❌ API_KEY አልተገኘም። .env ፋይልን ያረጋግጡ።")
        return False

    if not api_secret:
        print("❌ API_SECRET አልተገኘም። .env ፋይልን ያረጋግጡ።")
        return False

    if not base_url:
        print("❌ BASE_URL አልተገኘም። .env ፋይልን ያረጋግጡ።")
        return False

    print("\n==============================")
    print("🚀 FSE Exchange Connection Test")
    print("==============================")

    try:
        # Public ping endpoint - ይህ ለደህንነት ሲባል የንግድ ቁልፍ ሳይጠቀም የሚፈተሽ ነው
        endpoint = f"{base_url}/api/v1/ping"

        response = requests.get(
            endpoint,
            timeout=10
        )

        # Raise HTTP errors (4xx, 5xx)
        response.raise_for_status()

        print("✅ SUCCESS!")
        print("🌐 Exchange server is reachable.")
        print(f"📡 Status Code: {response.status_code}")

        return True

    except Timeout:
        print("⏳ Timeout Error: ሰርቨሩ በጊዜ ውስጥ መልስ አልሰጠም።")

    except ConnectionError:
        print("🌐 Connection Error: ከኤክስቼንጅ ሰርቨር ጋር መገናኘት አልተቻለም።")

    except HTTPError as err:
        print(f"⚠️ HTTP Error: {err}")

    except RequestException as err:
        print(f"❌ Request Error: {err}")

    except Exception as err:
        print(f"🔥 Unexpected Error: {err}")

    return False


# ==========================================
# Run Test
# ==========================================
if __name__ == "__main__":

    success = test_api_connection()

    if success:
        print("\n🟢 FSE API Connection Layer Ready!")
    else:
        print("\n🔴 FSE API Connection Test Failed!")
