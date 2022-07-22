if [[ -z "${TERMIN_ROOT}" ]]; then
  echo "TERMIN_ROOT is not env variable, creating one now"
else
  echo "TERMIN_ROOT is already exists, rewriting the env variable"
fi
TERMIN_ROOT=$(pwd)
echo "">>~/.bashrc
echo "# Environment variables for Termin project" >> ~/.zshrc
echo "export TERMIN_ROOT=$TERMIN_ROOT" >> ~/.zshrc

sudo mv chromedriver /usr/local/bin
sudo chmod 777 /usr/local/bin/chromedriver
mkdir log

rm -r venv
sleep 5
python3 -m venv venv
source venv/bin/activate
which python3
pip3 install -r requirements.txt
