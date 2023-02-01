library(shiny)

# shiny::runApp('/r-shiny-app', port = 3838)

CMD ["R", "-e", "shiny::runApp('/r-shiny-app', host='0.0.0.0', port=3838)"]