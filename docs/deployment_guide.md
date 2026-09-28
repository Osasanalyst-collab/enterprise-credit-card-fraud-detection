# Deployment
1. Train and approve a model. 2. Store artifacts in an immutable registry/object store. 3. Build and scan the Docker image. 4. Deploy to staging. 5. Run smoke/load/security tests. 6. Require approval. 7. Deploy canary, observe metrics, then promote. Secrets must come from a managed secret store.
