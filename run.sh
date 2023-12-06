if [[ ${DATA_TYPE} == edgex ]] || [[ ${DATA_TYPE} == video ]] ; then
  python3 -m pip install tensorflow
fi

echo success!