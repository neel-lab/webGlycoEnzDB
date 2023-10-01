library(shinydashboard)
library('visNetwork') 

header <- dashboardHeader(
  title = "GlycoTF",
  titleWidth = 300,  # Adjust the width as needed
  tags$li(
    class = "dropdown",
    a(
      href = "https://nam12.safelinks.protection.outlook.com/?url=https%3A%2F%2Fbiorxiv.org%2Fcgi%2Fcontent%2Fshort%2F2023.09.26.559616v1&data=05%7C01%7Cvghosh%40g-mail.buffalo.edu%7C8e664cf202964baca4f608dbc0855e94%7C96464a8af8ed40b199e25f6b50a20250%7C0%7C0%7C638315451290742529%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=MvUywYeLp4vSYphvWSc2IdQvteyVLcKRJot88WkkPpk%3D&reserved=0",
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
