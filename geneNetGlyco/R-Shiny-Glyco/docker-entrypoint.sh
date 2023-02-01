echo "Waiting for Database"
./wait-for-it.sh db:5433

echo "Starting shiny"

R -e shiny::runApp('/r-shiny-app', host='0.0.0.0', port=3838)