# 🧩 Zeo++ API Service

A production-ready FastAPI service that wraps [Zeo++](http://www.zeoplusplus.org/) structural analysis functionality as containerized HTTP endpoints.

---

## 🚀 Features

- ✅ Fully wraps all Zeo++ analysis options via HTTP API
- 🧠 Automatic caching via file content hash
- 📂 Structured output (JSON or raw `.res`, `.sa`, `.vol`, etc.)
- ⚙️ Configurable via `.env`
- 🐳 Docker-ready (auto-downloads + compiles Zeo++)
- 🎨 Rich logs and well-typed request/response models

---

## 📁 Project Structure

```text
app/
├── api/            # FastAPI route modules (one per Zeo++ feature)
├── models/         # Pydantic v2 request/response models
├── core/           # ZeoRunner, caching, config
├── utils/          # File saving, logging, output parser
├── main.py         # Entrypoint to register all routers
workspace/
├── tmp/            # Temporary run files
├── cache/          # Hashed result cache
```

---

## ⚙️ .env Example

```ini
ZEO_EXEC_PATH=network
ZEO_WORKSPACE=workspace
ENABLE_CACHE=true
LOG_LEVEL=INFO
```

---

## 🐳 Docker Compose

```yaml
version: "3.9"

services:
  zeopp-api:
    build: .
    ports:
      - "9876:8000"
    volumes:
      - ./workspace:/app/workspace
    env_file:
      - .env
```

Build and run:

```bash
docker compose up --build
```

---

## 🧪 Example: Call API via curl

```bash
curl -X POST http://localhost:9876/api/pore_diameter   -F "structure_file=@EDI.cssr"   -F "ha=true"   -F "output_filename=EDI.res"
```

Response:

```json
{
  "included_diameter": 4.89,
  "free_diameter": 3.03,
  "included_along_free": 4.81,
  "cached": false
}
```

---

## 📚 Supported Endpoints

| Route                     | Zeo++ Flag         | Output Type  | Format     |
|--------------------------|--------------------|--------------|------------|
| `/api/pore_diameter`     | `-res`             | 3 floats     | JSON       |
| `/api/surface_area`      | `-sa`              | ASA/NASA     | JSON       |
| `/api/accessible_volume` | `-vol`             | AV/NAV       | JSON       |
| `/api/probe_volume`      | `-volpo`           | POAV/PONAV   | JSON       |
| `/api/channel_analysis`  | `-chan`            | diameters    | JSON       |
| `/api/structure_info`    | `-strinfo`         | frameworks   | JSON       |
| `/api/pore_size_dist`    | `-psd`             | histogram    | Raw Text   |
| `/api/ray_tracing`       | `-ray_atom`        | histogram    | Raw Text   |
| `/api/blocking_spheres`  | `-block`           | spheres      | Raw Text   |
| `/api/distance_grid`     | `-grid*`           | .cube/.bov   | File       |
| `/api/voronoi_network`   | `-nt2 -r\|-nor`    | network      | Raw Text   |

---

## 🔒 Notes

- Accepts `.cssr`, `.cif`, `.pdb` structure files.
- Use `output_filename` to override default names.
- Logs and results are auto-organized under `workspace/`.
- Caching based on SHA256 file + args hash.

---

## 📜 License

MIT © Shibo Li, 2025
