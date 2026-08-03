# Eredivisie Soccer

Predictions, fixtures, standings, and team deep dives for the Dutch Eredivisie.

This is the Netherlands edition of Pitch Oracle. It has the same shared app
experience as the other league sites, with Eredivisie data, branding, and
league-specific configuration layered on top.

## Open the app

The live app is designed for Streamlit Cloud. Open it, choose a daytime or
nighttime theme, and use the sidebar to move between:

- Overview
- Predictions
- Standings
- Team Deep Dive

The app is refreshed from the repository's generated prediction cache. It does
not train models every time someone opens the page.

## First launch

After a new repository is created, the app may briefly show **Eredivisie setup
required**. That means the source code is ready, but the generated prediction
artifacts have not been built yet.

To prepare a new deployment:

1. Open the **Actions** tab on GitHub.
2. Select **Eredivisie artifact pipeline**.
3. Choose **Run workflow** on the `main` branch.
4. Wait for the run to finish successfully.
5. Reload or redeploy the Streamlit app.

The workflow gathers the latest available data, trains the league models,
precomputes predictions, validates the results, and commits the generated
cache back to `main`.

## Why this happens after repository creation

The app source and the prediction artifacts are two different things.

The source repository is small, reviewable, and reproducible. The artifacts are
generated files that can be large, change with new fixtures, and depend on live
data sources and the exact version of the shared Pitch Oracle package. Building
them is therefore a release step, not a file-copy step during initial setup.

This separation keeps a newly created league repository clean and lets the
artifact pipeline verify that the cache belongs to the Eredivisie before the
app serves it. Once the pipeline has committed a valid cache, the setup screen
should not appear again unless the generated artifacts are removed or a new
release is being prepared.

## Local development

Use Python 3.12 or newer. From the repository root:

```bash
python -m venv venv
venv\\Scripts\\python -m pip install -r requirements.txt
venv\\Scripts\\streamlit run predictions.py
```

For a clean local artifact build, run:

```bash
venv\\Scripts\\python scripts/bootstrap_local.py
```

That command downloads/prepares data, trains the models, builds the cache, and
runs the same consumer validation used before release. Data-provider access and
local environment setup may be required.

## Releasing an update

Run the artifact pipeline whenever the underlying data or shared app package
changes. A successful run should leave these generated areas updated:

- `data_files/` — source and derived league data
- `models/` — trained prediction models and diagnostics
- `precomputed/` — the feature cache and cache manifest

The pipeline also runs the consumer tests and refuses to publish an invalid or
wrong-league cache. Streamlit Cloud then picks up the commit from `main` and
restarts the app.

## If the app still shows the setup screen

Check that:

1. The latest **Eredivisie artifact pipeline** run succeeded.
2. `precomputed/cache_manifest.json` exists on `main`.
3. Streamlit Cloud is deploying the `main` branch and the correct entrypoint,
   `predictions.py`.
4. The app has been restarted or manually redeployed after the artifact commit.

## Project structure

```text
predictions.py       Streamlit entrypoint
config.py            Eredivisie configuration and theme choices
data_files/          Generated league data
models/              Generated model files
precomputed/         Generated prediction cache and manifest
scripts/              Local build and verification helpers
.github/workflows/    CI and scheduled artifact pipeline
```

The shared UI, data preparation, artifact contracts, and model pipeline live
in [`pitch-oracle-core`](https://github.com/gmalbert/pitch-oracle-core). This
repository intentionally contains only the Netherlands-specific layer and the
generated release cache.
