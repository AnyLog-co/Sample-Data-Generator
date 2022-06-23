for data in ping percentagecpu
do
  python3 data_generator.py 10.0.0.213:2051 ${data} file litsanleandro --repeat 3 --sleep 10 --batch-repeat 1000 --batch-sleep 10 --timezone local --enable-timezone-range &
done &

python3 data_generator.py 10.0.0.213:2051 opcua file aiops --repeat 3 --sleep 10 --batch-repeat 1000 --batch-sleep 1 --timezone ET --enable-timezone-range &

python3 data_generator.py 10.0.0.213:2051 linode file linode --repeat 3 --sleep 60 --batch-repeat 1 --batch-sleep 0 --timezone UTC &

python3 data_generator.py 10.0.0.213:2051 trig file test --repeat 3 --sleep 10 --batch-repeat 1000 --batch-sleep 0.5 --timezone JP &

for data in power synchrophasor
do
  python3 data_generator.py 10.0.0.213:2051 ${data} file afg --repeat 3 --sleep 10 --batch-repeat 1000 --batch-sleep 30 --timezone WS --enable-timezone-range &
done &



