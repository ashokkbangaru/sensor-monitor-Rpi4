#!/bin/bash

# Only run once to install and setup ngrok
echo "Installing ngrok..."
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo mv ngrok /usr/local/bin

echo "Paste your ngrok auth token:"
read TOKEN
ngrok config add-authtoken $TOKEN

echo "✅ ngrok is set up!"

