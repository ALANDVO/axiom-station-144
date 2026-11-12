# axiom-station-144

> Work in progress. This checkpoint may be incomplete or fail tests. See PLAN.md and STATUS.md before use.


Hunt down social media accounts by username across social networks (inspired by Sherlock).

## Installation

```bash
pip install -e .
```

## Usage

### CLI

Run the CLI via the module:

```bash
python -m src.sherlock <username> [--ssl/--no-ssl]
```

Example:

```bash
python -m src.sherlock john --no-ssl
```

### HTTP API

Start the FastAPI server:

```bash
uvicorn src.sherlock:fastapi_app --host 0.0.0.0 --port 8000
```

Then request:

```
GET /check?username=john
```

Returns JSON list of per-site results.

## Features

- Basic CLI for checking username on static sites (Twitter, Instagram, Reddit)
- Async site checking
- SSL verification toggle
- Simple HTTP API for integration

## Roadmap

See [PLAN.md](PLAN.md) for planned features.

## Contact

- Website: https://alanvo.net
- X: https://x.com/alanvoasi

## License

MIT

Maintainer: Alan Vo <alanvo@gmail.com>
