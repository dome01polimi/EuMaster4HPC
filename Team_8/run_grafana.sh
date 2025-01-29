#!/bin/sh

GRAFANA_DIR="grafana"

mkdir -p $GRAFANA_DIR $GRAFANA_DIR/data

# Check if container .sif file is present, if not build it from docker repo
if [ -e "$GRAFANA_DIR/grafana.sif" ]; then
	echo "grafana.sif is already present in $GRAFANA_DIR: skipping build."
else
	echo "grafana.sif is missing in $GRAFANA_DIR: starting to retrieve and build from docker://index.docker.io/grafana/grafana"
	singularity build $GRAFANA_DIR/grafana.sif docker://index.docker.io/grafana/grafana
	echo "Build finished"
fi

# Run the grafana container
singularity run \
	--bind $GRAFANA_DIR/data:/var/lib/grafana \
	--bind $GRAFANA_DIR/grafana.ini:/etc/grafana/grafana.ini \
	--bind $GRAFANA_DIR/dashboard.yaml:/etc/grafana/provisioning/dashboards/default.yaml \
	--bind $GRAFANA_DIR/datasource.yaml:/etc/grafana/provisioning/datasources/default.yaml \
    --bind $GRAFANA_DIR/dashboards:/var/lib/grafana/dashboards \
	--bind reframe_out:/reframe_out \
	--env GF_INSTALL_PLUGINS=marcusolsson-csv-datasource \
	$GRAFANA_DIR/grafana.sif grafana

# Clean-up the grafana files that can potentially collide with other users
rm -r $GRAFANA_DIR/data/grafana.db $GRAFANA_DIR/data/csv $GRAFANA_DIR/data/pdf $GRAFANA_DIR/data/plugins $GRAFANA_DIR/data/png