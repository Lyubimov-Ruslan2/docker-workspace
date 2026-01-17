# NYC Taxi Data Ingestion Pipeline

A containerized data pipeline for ingesting NYC yellow taxi trip data into a PostgreSQL database. Built with Docker, Python, and Click CLI.

## Overview

This project automates the process of downloading NYC taxi datasets from the [DataTalks Club repository](https://github.com/DataTalksClub/nyc-tlc-data) and loading them into a PostgreSQL database in chunks for efficient processing of large datasets.

## Architecture

```
┌─────────────────┐
│  Taxi CSV Data  │ (Remote GitHub Release)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│  ingest_data.py             │ (Click CLI Parameters)
│  - Download & Parse         │
│  - Stream in Chunks         │
│  - Insert into Postgres     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  PostgreSQL (Docker Service)│
│  - ny_taxi database         │
│  - yellow_taxi_data table   │
└─────────────────────────────┘
```

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.13+ (for local development)
- `uv` package manager (optional, for local development)

### Using Docker Compose

1. **Start Services**
   ```bash
   cd pipeline
   docker-compose up -d
   ```
   This starts:
   - PostgreSQL 18 on `localhost:5432` (credentials: root/root)
   - pgAdmin on `localhost:8085` (email: admin@admin.com, password: root)

2. **Run Data Ingestion**
   ```bash
   docker-compose exec pgdatabase psql -U root -d ny_taxi -c "SELECT COUNT(*) FROM yellow_taxi_data;"
   ```

3. **Stop Services**
   ```bash
   docker-compose down
   ```

### Using Docker Image Directly

Build and run the ingest container:
```bash
cd pipeline
docker build -t taxi_ingest:v001 .

docker run -it --rm \
  --network=pipeline_default \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=pgdatabase \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --year=2021 \
  --month=1 \
  --target-table=yellow_taxi_data \
  --chunksize=100000
```

### Local Development

1. **Install Dependencies**
   ```bash
   cd pipeline
   uv sync
   ```

2. **Run Ingestion Script with CLI Options**
   ```bash
   uv run python ingest_data.py --help
   ```

## CLI Parameters

The `ingest_data.py` script accepts the following Click CLI options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--pg-user` | TEXT | `root` | PostgreSQL username |
| `--pg-pass` | TEXT | `root` | PostgreSQL password |
| `--pg-host` | TEXT | `localhost` | PostgreSQL host |
| `--pg-port` | INTEGER | `5432` | PostgreSQL port |
| `--pg-db` | TEXT | `ny_taxi` | PostgreSQL database name |
| `--year` | INTEGER | `2021` | Dataset year (e.g., 2021) |
| `--month` | INTEGER | `1` | Dataset month (1-12) |
| `--target-table` | TEXT | `yellow_taxi_data` | Destination table name |
| `--chunksize` | INTEGER | `100000` | Rows per chunk (memory efficiency) |
| `--prefix` | TEXT | DataTalks URL | Base URL for dataset download |

### Examples

**Ingest January 2021 data (defaults):**
```bash
uv run python ingest_data.py
```

**Ingest March 2022 data with custom chunk size:**
```bash
uv run python ingest_data.py --year=2022 --month=3 --chunksize=50000
```

**Ingest to custom table:**
```bash
uv run python ingest_data.py --target-table=taxi_trips_staging
```

## Project Structure

```
docker-workspace/
├── README.md                          # This file
├── pipeline/
│   ├── ingest_data.py                # Main ingestion script (Click CLI)
│   ├── main.py                        # Entry point
│   ├── pipeline.py                    # Utility functions
│   ├── Dockerfile                     # Container image definition
│   ├── docker-compose.yaml            # Multi-container orchestration
│   ├── pyproject.toml                 # Python dependencies
│   ├── notebook.ipynb                 # Jupyter notebook for exploration
│   └── README.md                      # Pipeline-specific documentation
├── ny_taxi_postgres_data/             # Docker volume for persistent data
└── test/                              # Test files
```

## Database Schema

The default table `yellow_taxi_data` contains the following columns:

- `VendorID` (Int64): Vendor identifier
- `tpep_pickup_datetime` (Timestamp): Pickup time
- `tpep_dropoff_datetime` (Timestamp): Dropoff time
- `passenger_count` (Int64): Number of passengers
- `trip_distance` (float64): Trip distance in miles
- `PULocationID` (Int64): Pickup location zone ID
- `DOLocationID` (Int64): Dropoff location zone ID
- `RatecodeID` (Int64): Rate code
- `payment_type` (Int64): Payment method
- `fare_amount` (float64): Base fare
- `extra` (float64): Extra charges
- `mta_tax` (float64): MTA tax
- `tip_amount` (float64): Tip amount
- `tolls_amount` (float64): Tolls
- `improvement_surcharge` (float64): Improvement surcharge
- `total_amount` (float64): Total trip amount
- `congestion_surcharge` (float64): Congestion surcharge

## Technologies

- **Python 3.13**: Core programming language
- **Click**: CLI framework for parameter management
- **Pandas**: Data processing and CSV handling
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Data warehouse
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **pgAdmin**: PostgreSQL web interface
- **tqdm**: Progress bars

## Development

### Running Tests
```bash
cd pipeline
uv run pytest
```

### Database Access

**pgAdmin Web UI:**
- URL: http://localhost:8085
- Email: admin@admin.com
- Password: root

**Direct psql Connection:**
```bash
psql -h localhost -U root -d ny_taxi
```

### Monitoring Ingestion

Connect to PostgreSQL and check table size:
```sql
SELECT 
  relname as table_name,
  pg_size_pretty(pg_total_relation_size(relid)) as size
FROM pg_stat_user_tables
WHERE relname = 'yellow_taxi_data';
```

## Common Issues

**Connection refused to localhost:5432**
- Ensure Docker Compose services are running: `docker-compose ps`
- Check PostgreSQL logs: `docker-compose logs pgdatabase`

**Out of memory during ingestion**
- Reduce `--chunksize` parameter to process fewer rows at once
- Example: `--chunksize=50000`

**Download timeout**
- Check internet connection and GitHub availability
- Try with `--prefix` pointing to alternative data source if needed

## Data Source

NYC taxi data is provided by DataTalks Club and sourced from the [NYC Taxi and Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

Available datasets:
- Yellow Taxi Trips
- Green Taxi Trips  
- For-Hire Vehicle Trips

## License

This project is provided for educational purposes.

## Contributing

For questions or improvements, please open an issue or submit a pull request.