# install programs
if [[ ${INSERT_PROCESS} == mqtt ]] ; then
  python3 -m pip install paho-mqtt
fi
if [[ ${DATA_TYPE} == edgex ]] || [[ ${DATA_TYPE} == video ]] ; then
  python3 -m pip install --upgrade numpy opencv-python
  python3 -m pip install tensorflow numpy
elif [[ ${CONVERSION_TYPE} == opencv ]] ; then
  python3 -m pip install --upgrade opencv-python numpy
fi

# Validate values
if [[ ${DATA_TYPE} == node_insight ]] && [[ ${INSERT_PROCESS} == mqtt ]] ; then
  echo "node_insight requires using REST for data processing"
  exit 1
fi


echo success!