library(shinydashboard)
library('visNetwork') 

header <- dashboardHeader(
  title = "GlycoNet"
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
               textAreaInput('target_genes', 'Target Genes', value = "", width = NULL, height = "150px",
                             cols = NULL, rows = NULL, placeholder = "Target Genes (newline seperated)", resize = NULL),
               # textAreaInput('transcription_factors', 'Transcription Factors', value = "", width = NULL, height = "150px",
               #               cols = NULL, rows = NULL, placeholder = "Transcription Factors (newline seperated)", resize = NULL),
               numericInput('percentile', "NMI (normalized mutual information)", value=99, min = 0, max = 100, width = NULL),
               actionButton("searchButton", "Search")
           ),
           box(width = NULL, status = "warning",
               DT::dataTableOutput('top_tfs')
           ),
           box(width = NULL, status = "warning",
               actionButton("deselect_all", "Deselect All"),
               uiOutput("checkbox")
           ),
    )
  )
)

dashboardPage(
  header,
  dashboardSidebar(disable = TRUE),
  body
)


# https://rstudio.github.io/DT/shiny.html
