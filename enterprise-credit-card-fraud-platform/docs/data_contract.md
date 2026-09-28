# Data contract
The required PaySim-style fields are listed in `fraud_detection.config.constants.RAW_COLUMNS`. Amount and balances must be non-negative; transaction IDs should be tokenised before production storage; labels are optional at real-time inference but required for training.
