# Charged

Challenge 9: **Monitoring and management of railway vehicle batteries**.

<p align="center">
  <img alt="Charged: Battery Monitoring" src="img/charged_screenshot.png" width="800"/>
</p>

## Background

<p align="center">
  <img alt="Hack4Rail Logo" src="img/hack4rail-logo.jpg" width="150"/>
</p>

This project has been initiated during the [Hack4Rail 2025](https://hack4rail.event.sbb.ch/en/), a joint hackathon organised by the railway companies SBB, ÖBB, and DB in partnership with the OpenRail Association.

## Install

Install virtual environment for Python:

```bash
make
```

Create `.env` and update according to the documentation to enable database connection.


Start dashboard:

```bash
# load data from database to local parquet file.
uv run python dashboard/preprocess_data.py
# run stramlit dashboard
uv run streamlit run dashboard/main.py
```

## License

<!-- If you decide for another license, please change it here, and exchange the LICENSE file -->

The content of this repository is licensed under the [Apache 2.0 license](LICENSE).
