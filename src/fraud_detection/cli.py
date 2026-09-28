import argparse, json
from fraud_detection.config.settings import get_settings
from fraud_detection.inference.predictor import FraudPredictor
from fraud_detection.ingestion.batch_ingestion import read_csv
from fraud_detection.pipeline import run_training_pipeline
from fraud_detection.utils.logger import configure_logging

def main():
    parser = argparse.ArgumentParser(description="Enterprise fraud detection workflow")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run-all"); run.add_argument("--input", required=True); run.add_argument("--model", default="logistic"); run.add_argument("--sample-rows", type=int)
    score = sub.add_parser("score"); score.add_argument("--input", required=True); score.add_argument("--output", default="artifacts/predictions.csv")
    args = parser.parse_args(); settings = get_settings(); configure_logging(settings.log_level)
    if args.command == "run-all":
        print(json.dumps(run_training_pipeline(args.input, args.model, args.sample_rows), indent=2, default=str))
    else:
        raw = read_csv(args.input); result = FraudPredictor(settings.model_dir).predict_frame(raw); result.to_csv(args.output, index=False); print(f"Saved {len(result):,} predictions to {args.output}")

if __name__ == "__main__": main()
