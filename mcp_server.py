"""MCP Server for STFT Spectrogram Skill."""
import json
import sys
from client import STFTAnalyzer

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": [{
                            "name": "generate_spectrogram",
                            "description": "Generate time-frequency spectrogram using STFT",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "signal": {"type": "array", "items": {"type": "number"}},
                                    "window_size": {"type": "integer"},
                                    "hop_size": {"type": "integer"}
                                },
                                "required": ["signal"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                args = params.get("arguments", {})
                spec = STFTAnalyzer.compute_spectrogram(
                    signal=args["signal"],
                    window_size=args.get("window_size", 4),
                    hop_size=args.get("hop_size", 2)
                )
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": json.dumps({"spectrogram": spec, "frames": len(spec)})}]}
                }
            else:
                res = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            print(json.dumps(res), flush=True)
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err), flush=True)

if __name__ == "__main__":
    main()
