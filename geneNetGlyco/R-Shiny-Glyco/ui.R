library(shinydashboard)
library('visNetwork') 

header <- dashboardHeader(
  title = "GlycoTF",
  titleWidth = 300,  # Adjust the width as needed
  tags$li(
    class = "dropdown",
    a(
      href = "https://www.biorxiv.org/content/10.1101/2023.09.26.559616v1",
      target = "_blank",  # Open link in a new tab
      icon("external-link"),
      "bioRxiv Link"
    )
  )
)

body <- dashboardBody(
  fluidRow(
    column(width = 9,
           box(width = NULL, solidHeader = TRUE,
               visNetworkOutput("mynetworkid", height = '600px'),
               sliderInput("max_nodes", "Nodes",
                           min = 1, max = 2000,
                           value = 200)
           ),
           box(width = NULL,
               DT::dataTableOutput('table')
           )
    ),
    column(width = 3,
           box(width = NULL, status = "warning",
               #uiOutput("cell_main"),
               uiOutput("glycopath"),
               textAreaInput('target_genes', 'Glycogenes', value = "", width = NULL, height = "150px",
                             cols = NULL, rows = NULL, placeholder = "Glycogenes (newline seperated)", resize = NULL),
               # textAreaInput('transcription_factors', 'Transcription Factors', value = "", width = NULL, height = "150px",
               #               cols = NULL, rows = NULL, placeholder = "Transcription Factors (newline seperated)", resize = NULL),
               numericInput('percentile', "NMI Pct. Threshold", value=99, min = 0, max = 100, width = NULL),
               actionButton("searchButton", "Search")
           ),
           box(width = NULL, status = "warning",
               actionButton("deselect_all", "Deselect All"),
               actionButton("select_all", "Select All"),
               uiOutput("checkbox")
           ),
           box(width = NULL, status = "warning",
               DT::dataTableOutput('top_tfs')
           ),
    )
  ),
  tags$head(tags$style(HTML('
      .skin-blue .main-header .navbar{
        background-color: #005bbb;
      }
      
      .skin-blue .main-header .logo{
        background-color: #005bbb;
      }
    ')))
)

dashboardPage(
  header,
  dashboardSidebar(disable = TRUE),
  body,
)


# https://rstudio.github.io/DT/shiny.html
