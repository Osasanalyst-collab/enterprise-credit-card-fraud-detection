# Session-by-session build order

1. Environment setup
2. Dataset placement or safe sample generation
3. Ingestion and schema validation
4. Cleaning and standardisation
5. Corrected feature engineering
6. Baseline model training
7. Candidate model training
8. Batch inference
9. Database persistence
10. Data-quality monitoring
11. FastAPI service
12. Airflow, Docker and CI/CD
13. Final end-to-end production workflow

Run from the repository root:
```bash
python sessions/01_environment_setup.py
python sessions/02_generate_or_place_dataset.py
# Continue in numerical order.
```
