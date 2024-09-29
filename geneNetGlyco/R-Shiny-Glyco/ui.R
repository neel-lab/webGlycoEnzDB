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
  ),
  tags$li(
    class = "dropdown",
    a(
      href = "mailto:rgunawan@buffalo.edu",
      target = "_blank",  # Open email link in a new tab
      icon("envelope"),  # Font Awesome mail icon
      "Contact us"
    )
  ),
  tags$li(
    class = "dropdown",
    downloadLink("downloadPDFManual", HTML(paste0("User Manual &nbsp;", icon("download"))))
  )
)

body <- dashboardBody(
  fluidRow(
    column(width = 9,
           box(width = NULL, solidHeader = TRUE,
               visNetworkOutput("mynetworkid", height = '600px'),
               sliderInput("max_nodes", "TF-Gene Linkage",
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
               textAreaInput('target_genes', 'Enter genes (one gene per row):', value = "", width = NULL, height = "150px",
                             cols = NULL, rows = NULL, placeholder = "", resize = NULL),
               # textAreaInput('transcription_factors', 'Transcription Factors', value = "", width = NULL, height = "150px",
               #               cols = NULL, rows = NULL, placeholder = "Transcription Factors (newline seperated)", resize = NULL),
               numericInput('percentile', "MI Pct. Threshold", value=99, min = 0, max = 100, width = NULL),
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
