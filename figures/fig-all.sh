#! /bin/bash
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

# example figures
bash ${SCRIPTPATH}/fig-teaser.sh &
bash ${SCRIPTPATH}/fig-myles-examples.sh &
bash ${SCRIPTPATH}/fig-tetwild-examples.sh &

wait

# test figures
bash ${SCRIPTPATH}/fig-stress-test.sh &
bash ${SCRIPTPATH}/fig-quality.sh &

exit

wait

# dataset plot figures
bash ${SCRIPTPATH}/fig-performance.sh
bash ${SCRIPTPATH}/fig-myles-dataset.sh
bash ${SCRIPTPATH}/fig-tetwild-datatset.sh


