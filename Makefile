.PHONY: help install query-significant query-worldwide query-recent query-custom

# Default Python command
PYTHON := python3
SCRIPT := main.py

# Help target
help:
	@echo "Earthquake USGS Query Tool"
	@echo ""
	@echo "Available targets:"
	@echo "  query-significant - Query significant earthquakes worldwide (mag >= 6.0)"
	@echo "  query-worldwide   - Query all earthquakes worldwide (last 30 days)"
	@echo "  query-recent      - Query recent earthquakes (last 7 days, mag >= 4.0)"
	@echo "  query-custom      - Run custom query with flexible arguments (supports --monthly flag)"
	@echo "  clean             - Remove generated data files"
	@echo ""
	@echo "Examples:"
	@echo "  make query-custom ARGS='--starttime 2024-01-01 --minmagnitude 5.0'"
	@echo "  make query-custom ARGS='--starttime 2001-01-01 --endtime 2025-10-22 --monthly'"
	@echo "  make query-custom ARGS='--latitude 37.7749 --longitude -122.4194 --maxradiuskm 100'"

# Query significant earthquakes worldwide
query-significant:
	$(PYTHON) $(SCRIPT) \
		--minmagnitude 6.0 \
		--orderby magnitude \
		--limit 100

# Query all earthquakes worldwide (last 30 days)
query-worldwide:
	$(PYTHON) $(SCRIPT) \
		--orderby time \
		--limit 1000

# Query recent earthquakes (last 7 days, mag >= 4.0)
query-recent:
	$(PYTHON) $(SCRIPT) \
		--starttime $(shell date -v-7d +%Y-%m-%d) \
		--minmagnitude 4.0 \
		--orderby time

# Custom query - set ARGS variable with all desired arguments
query-custom:
	$(PYTHON) $(SCRIPT) $(ARGS)

# Clean generated data files
clean:
	rm -rf dataset/raw/*.json dataset/raw/*.csv dataset/raw/*.xml dataset/raw/*.kml dataset/raw/*.txt

# Advanced queries
query-japan:
	$(PYTHON) $(SCRIPT) \
		--minlatitude 30 \
		--maxlatitude 46 \
		--minlongitude 128 \
		--maxlongitude 146 \
		--minmagnitude 4.0 \
		--orderby time

query-alaska:
	$(PYTHON) $(SCRIPT) \
		--minlatitude 50 \
		--maxlatitude 72 \
		--minlongitude -180 \
		--maxlongitude -130 \
		--minmagnitude 3.0 \
		--orderby time

query-pacific-ring:
	$(PYTHON) $(SCRIPT) \
		--minlatitude -60 \
		--maxlatitude 60 \
		--minlongitude 140 \
		--maxlongitude -120 \
		--minmagnitude 5.0 \
		--orderby magnitude \
		--limit 200

query-depth-shallow:
	$(PYTHON) $(SCRIPT) \
		--maxdepth 50 \
		--minmagnitude 4.0 \
		--orderby time

query-depth-deep:
	$(PYTHON) $(SCRIPT) \
		--mindepth 300 \
		--minmagnitude 5.0 \
		--orderby magnitude