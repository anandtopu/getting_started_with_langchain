# Local container rehearsal

Set distinct `API_CUSTOMER_TOKEN` and `API_MANAGER_TOKEN` values in the ignored `.env` file using the setup instructions. Keep `COURSE_OFFLINE=true` for the rehearsal. Never bake credentials into the image.

```text
docker build -f capstones/02_support_copilot/Dockerfile -t brightwave-copilot .
docker run --rm --read-only --tmpfs /tmp:rw,nosuid,size=256m --tmpfs /runtime:rw,mode=1777,size=64m --env-file .env -p 127.0.0.1:8000:8000 brightwave-copilot
```

Build from the repository root. The image includes shared code and synthetic seed data, runs as UID 10001, uses one worker, and writes only runtime state. The temporary runtime disappears when the container stops. For persistence, provision a protected writable volume owned by UID 10001; backups and retention are operator responsibilities. This is a local rehearsal, not a cloud deployment. The separate [production lesson](../../modules/20_production/README.md) explains persistent storage and the Postgres probe. The customer answer-quality gate must pass before deployment to customers.
