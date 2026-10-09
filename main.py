import json
from fastapi import FastAPI

CHUNKS = {
    "A": ["7b22726573706f6e736522", "3a225265706f7274206a6f622d66386330303332343a",
          "20222c22646f6e65223a66616c73657d0a7b",
          "227468696e6b696e67223a22696e7465726e616c206e6f",
          "7465222c22726573706f6e7365223a22222c2264",
          "6f6e65223a66616c73657d0a7b22", "726573706f6e7365223a22636166c3",
          "a95c6e222c22646f6e65223a66616c7365",
          "7d0a7b22726573706f6e7365223a22526561647920", "e2",
          "9c93222c22646f6e65223a747275652c22",
          "646f6e655f726561736f6e223a2273746f70227d0a"],
    "B": ["7b22726573706f6e736522", "3a225061727469616c206a6f622d6638633030333234",
          "222c22646f6e65223a66616c73657d0a7b22",
          "726573706f6e7365223a22756e66696e6973686564"],
    "C": ["7b22726573706f6e736522", "3a224472616674206a6f622d6638633030333234222c",
          "22646f6e65223a66616c73657d0a7b226572",
          "726f72223a226d6f64656c20756e6c6f61646564227d0a",
          "7b22726573706f6e7365223a2249474e4f524522",
          "2c22646f6e65223a747275657d0a"],
}


def decode(chunks):
    raw = b"".join(bytes.fromhex(c) for c in chunks)
    lines = raw.split(b"\n")[:-1]  # last piece has no newline: incomplete, ignored
    text = ""
    for line in lines:
        if not line.strip():
            continue
        try:
            rec = json.loads(line.decode("utf-8"))
        except Exception:
            continue
        if rec.get("error"):
            return {"text": text, "complete": False, "error": rec["error"]}
        text += rec.get("response", "")
        if rec.get("done") is True:
            return {"text": text, "complete": True, "error": None}
    return {"text": text, "complete": False, "error": None}


ANSWER = {k: decode(v) for k, v in CHUNKS.items()}

app = FastAPI()


@app.get("/")
def root():
    return ANSWER


@app.get("/answer")
def answer():
    return ANSWER
