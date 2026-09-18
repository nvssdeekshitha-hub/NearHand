import asyncio
import json
import urllib.request
import websockets

async def test_websocket_flow():
    # User 2 is Senior Lakshmi
    uri = "ws://127.0.0.1:8000/ws/2"
    print(f"Connecting to NearHand WebSocket at {uri}...")

    async with websockets.connect(uri) as ws:
        # 1. Receive connection handshake
        greeting = await ws.recv()
        print("\n[WS EVENT RECEIVED]:", json.dumps(json.loads(greeting), indent=2))

        # 2. Trigger critical request in background thread
        print("\nTriggering POST /demo/simulate-critical-request...")
        req = urllib.request.Request(
            "http://127.0.0.1:8000/demo/simulate-critical-request",
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("HTTP POST Result:", data["message"])

        # 3. Listen for WebSocket broadcast events
        print("\nWaiting for real-time WebSocket events...")
        for _ in range(3):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=5.0)
                event_obj = json.loads(msg)
                print(f"\n[WS EVENT '{event_obj.get('event')}'] Received:")
                print(json.dumps(event_obj, indent=2))
            except asyncio.TimeoutError:
                break

if __name__ == "__main__":
    asyncio.run(test_websocket_flow())
