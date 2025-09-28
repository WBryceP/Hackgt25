import sys
import json
import httpx


def main():
	url = sys.argv[1] if len(sys.argv) > 1 else "https://link.testfile.org/lfSv97"
	service_base = "http://127.0.0.1:8000"
	try:
		with httpx.Client(timeout=120) as client:
			health = client.get(f"{service_base}/health")
			if health.status_code != 200:
				print(f"Service not healthy: {health.status_code} {health.text}")
				return 1
			resp = client.post(
				f"{service_base}/embed",
				json={"downloadUrl": url},
			)
			print(json.dumps(resp.json(), indent=2))
			return 0
	except Exception as e:
		print(f"Error: {e}")
		return 1


if __name__ == "__main__":
	raise SystemExit(main())
