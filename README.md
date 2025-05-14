# Zeo++ API Service

A production-ready FastAPI service that wraps [Zeo++](http://www.zeoplusplus.org/) structural analysis functionality as containerized HTTP endpoints.

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
├── api/            # All FastAPI route modules (one per Zeo++ feature)
├── models/         # Pydantic request/response models
├── core/           # Runner + config
├── utils/          # File save, logging, Zeo++ output parser
├── main.py         # Entrypoint to register all routers
workspace/          # tmp/ and cache/ for intermediate files
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

## 🐳 Docker Build

```bash
docker build -t zeopp-api .
docker run -it --rm -p 8000:8000 zeopp-api
```

---

## 🧪 Example: Call API via curl

```bash
curl -X POST http://localhost:8000/api/pore_diameter \
  -F "structure_file=@EDI.cssr" \
  -F "ha=true" \
  -F "output_filename=EDI.res"
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

## 🧠 Supported Endpoints

| Route                     | Zeo++ Flag         | Returns         |
|--------------------------|--------------------|------------------|
| `/api/pore_diameter`     | `-res`             | JSON             |
| `/api/surface_area`      | `-sa`              | JSON             |
| `/api/accessible_volume` | `-vol`             | JSON             |
| `/api/probe_volume`      | `-volpo`           | JSON             |
| `/api/channel_analysis`  | `-chan`            | JSON             |
| `/api/structure_info`    | `-strinfo`         | JSON             |
| `/api/oms_detection`     | `-oms`             | JSON             |
| `/api/pore_size_dist`    | `-psd`             | Raw text         |
| `/api/ray_tracing`       | `-ray_atom`        | Raw text         |
| `/api/blocking_spheres`  | `-block`           | Raw text         |
| `/api/distance_grid`     | `-grid*`           | Raw text (file)  |
| `/api/convert_xyz`       | `-xyz`             | XYZ text         |
| `/api/voronoi_network`   | `-nt2 -r|-nor`     | Raw text         |

---

## 🔒 Notes

- API accepts `.cssr`, `.cif`, `.pdb` structure files.
- Use `output_filename` form field to customize file naming.
- Caching is SHA256-based and automatic.

---

## 📜 License

MIT © Shibo Li, 2025
