# Eredivisie Soccer

![Pitch Oracle Eredivisie](data_files/logo.png)

## Follow Dutch football with more context

The Eredivisie is the Netherlands’ top-flight football competition: an open,
technical league known for strong club identities, attacking football, and a
steady stream of emerging talent. Pitch Oracle brings that competition into a
single place for supporters who want more than a scoreline.

Explore the race for the title, European places, and survival through a clear
view of the league’s fixtures, form, standings, and team-level storylines.

## What you can explore

- **Overview:** See the latest league picture at a glance, including upcoming
  fixtures and historical context.
- **Predictions:** Review match forecasts, confidence, risk, and the available
  recommendation for each upcoming game.
- **Standings:** Follow the table and the changing shape of the season.
- **Team Deep Dive:** Compare clubs through recent form, performance trends,
  strengths, and weaknesses.
- **Statistics and Model Lab:** Dig into league patterns and understand the
  evidence behind the forecasts.

The Netherlands edition of Pitch Oracle combines current Eredivisie fixtures
with historical results, team form, match conditions, and other football
signals. It is designed to help fans ask better questions about the league,
not to replace their judgment.

## Open the app

The live app is designed for Streamlit Cloud. Open it, choose a daytime or
nighttime theme, and use the sidebar to move between:

- Overview
- Predictions
- Standings
- Team Deep Dive

The app is refreshed from the repository's generated prediction cache. It does
not train models every time someone opens the page.

## Streamlit Cloud setup

Deploy this app with **Python 3.12**.

The shared prediction stack includes scientific packages with compiled
dependencies. Python 3.14 can cause Streamlit Cloud's resolver to select an
old `llvmlite` build that cannot run on Python 3.14, resulting in an error
before the app starts. Python 3.12 is the supported deployment target for this
release and matches the CI and artifact pipeline environment.

When creating the Streamlit app, open **Advanced settings**, select **Python
3.12**, and deploy from the `main` branch with `predictions.py` as the app
file. If the app already exists on another Python version, Streamlit Cloud
requires deleting and redeploying it to change the Python version; changing
`requirements.txt` alone is not enough.

The requirements use PyTorch's CPU-only wheel. Streamlit Cloud does not have a
GPU, so downloading NVIDIA/CUDA packages is unnecessary and can make startup
dramatically slower. The neural models still run on CPU when those optional
features are used.

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

Use Python 3.12 locally so development matches Streamlit Cloud and GitHub
Actions. From the repository root:

The local bootstrap loads provider credentials from the ignored `.env` file.
Use `.env.example` as the variable-name contract. This repository's `.env` was
copied from the local `pitch-oracle-core` checkout and must never be committed.

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

For GitHub Actions, configure the required names from `.env.example` as
repository or organization secrets. The workflow passes them to the shared core
through `secrets: inherit`; local `.env` files are never uploaded to Actions.

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
