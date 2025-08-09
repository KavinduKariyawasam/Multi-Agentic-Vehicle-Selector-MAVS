import requests
from utils.config import API_BASE_URL, API_TIMEOUT_SECONDS

class APIClient:
    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_TIMEOUT_SECONDS):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health_check(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=10)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def get_recommendations(self, location: str, budget: str, allowed_sites=None):
        payload = {
            "location": location,
            "budget": budget,
            "allowed_sites": allowed_sites or [],
        }
        try:
            r = requests.post(
                f"{self.base_url}/api/recommend",
                json=payload,
                timeout=self.timeout,  # now 300s by default
            )
            r.raise_for_status()
            return r.json()
        except requests.Timeout:
            return {"ok": False, "error": f"Request timed out after {self.timeout}s."}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}
