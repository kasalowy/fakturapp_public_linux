# fakturapp
Dockerized app designed to download and extract data from fakturownia.pl   

REQUIREMENTS:
 - Docker
 - jq (JSON shell tool)

The app allows for running extraction, transformation and export of data from fakturownia.pl account, all in an isolated docker environment. Fakturapp was designed to create docker image and container on top of it, every time it is run. After each run, successful or not, both image and container are deleted (in order to change that, edit main.sh file).

By default, Fakturapp is run by typing following command:

    sudo bash main.sh
For the app to build succesful connection with fakurownia.pl, config file has to be filled with both domain address and api token.
