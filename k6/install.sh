#!/bin/bash 
sudo apt update

sudo apt install apt-transport-https ca-certificates gnupg curl
curl -s https://dl.k6.io/key.gpg | sudo apt-key add -
echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list

sudo apt update
sudo apt install k6

k6 version

