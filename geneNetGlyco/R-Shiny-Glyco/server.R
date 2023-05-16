library(DBI)
library('visNetwork')
library(RPostgres)


db_url = "localhost" #Sys.getenv(c("DB_URL"))

database_name = "glycogenes"   # Specify the name of your Database
# Specify host name e.g.:"aws-us-east-1-portal.4.dblayer.com"
db_host = db_url  
db_port = "5432"                # Specify your port number. e.g. 98939
db_uid = "postgres"         # Specify your username. e.g. "admin"
db_pwd = "847468"        # Specify your password. e.g. "xxx"
cell_type_config_file = "../configs/cell_types_dropdown_config_glyco.csv"
glycoEnzOnto_file = "../configs/glycoEnzKO.csv"

con <- dbConnect(RPostgres::Postgres(),
                 dbname = database_name,
                 host = db_host,
                 port = db_port,
                 user = db_uid,
                 password = db_pwd)
cell_main_types = read.csv(cell_type_config_file)
glycoEnzOnto = read.csv(glycoEnzOnto_file)

rv <- reactiveValues()

function(input, output, session) {
  
  get_data <- reactive({
    
    cell_types = cell_main_types[cell_main_types['tissue'] == 'all', 'cell_type_id']
    # cell_types = cell_main_types[cell_main_types['tissue'] == input$choose_main & cell_main_types['cellType'] == input$choose_subtype, 'cell_type_id']
    tags_txt = paste0(shQuote(cell_types), collapse=", ")
    #print(tags_txt)
    
    #glycogenes = glycoEnzOnto[!glycoEnzOnto[input$choose_path]=="", input$choose_path]
    glycogenes = apply(glycoEnzOnto[input$choose_path], 1, function(x) paste(x[!is.na(x)], collapse = ", ")) 
    glycogenes = glycogenes[!glycogenes==""]
    
    percentile = input$percentile*1e-2
    
    output$checkbox <- renderUI({
      checkboxGroupInput("checkbox","Genes in Pathway", choices = glycogenes, selected = glycogenes)
    })
    # print(glycogenes)
    
    glycogenes_txt = paste0(shQuote(glycogenes), collapse=", ") 
    target_gene_list = unlist(strsplit(toupper(input$target_genes), split="\n"))
    target_gene_txt = paste0(shQuote(target_gene_list), collapse=", ")
    
    if (length(target_gene_list) == 0 && length(glycogenes) > 0) all_gene_txt = glycogenes_txt
    if (length(target_gene_list) > 0 && length(glycogenes) == 0) all_gene_txt = target_gene_txt
    if (length(target_gene_list) > 0 && length(glycogenes) > 0) all_gene_txt = paste(glycogenes_txt, target_gene_txt, sep = ", ")
    
    
    query <- paste("with dataset as (
select tf, target, confidence from TF_Glyco where cell_type_id in (
",tags_txt, ")), dataset_filtered as ( 
select * from dataset where confidence >= (select percentile_disc(",percentile,") WITHIN GROUP (ORDER BY confidence) from dataset))
select * from dataset_filtered", 
                   if (length(target_gene_list) > 0 || length(glycogenes) > 0) paste('where target in (', all_gene_txt, ')') else ""
    )
    
    cell_type <- dbSendQuery(con, query)
    result = dbFetch(cell_type)
    result = result[order(-result$confidence),]
    result
  })
  
  render_page <- function() {
    
    output$table <- DT::renderDataTable(
      DT::datatable(rv$selected_result, options = list(pageLength = 25), 
                    #selection = list(mode = 'multiple', selected = 1:100)
      )
    )
    
    value_count <-as.data.frame(table(rv$selected_result$tf))
    
    value_count = value_count[order(-value_count$Freq),]
    
    output$top_tfs <- DT::renderDataTable(DT::datatable(value_count))
    
    output$mynetworkid <- renderVisNetwork({
      
      # If data is empty, return empty
      if (nrow(rv$selected_result) == 0) {
        return(NULL)
      }
      # print(nrow(rv$selected_result))
      
      
      result_top100 = head(rv$selected_result, input$max_nodes)
      links <- result_top100
      names(links)[1] <- "from"
      names(links)[2] <- "to"
      
      #from_nodes = as.data.frame(unique(links$from), col.names = c('id'), color.background = "red") 
      #to_nodes = as.data.frame(unique(links$to), col.names = c('id'), color.background = "lightblue") 
      
      #id = union(from_nodes,to_nodes)
      #print(from_nodes)
      
      target_genes = unique(links$to)
      
      id = union(links$from,links$to)
      
      nodes <- data.frame(id)
      # nodes$color.background <- ifelse(nodes$id %in% target_genes, "red", "lightblue")
      nodes$group <- ifelse(nodes$id %in% target_genes, "Target", "TF")
      nodes$font.size = 50
      nodes$hidden = FALSE
      # nodes$shape = 'circle'
      # print(nodes)
      # nodes <- data.frame(id = 1:10, color = c(rep("blue", 6), rep("red", 3), rep("green", 1)))
      
      target_nodes = nodes[nodes$group == "Target", ]
      tf_nodes = nodes[nodes$group == "TF", ]
      # target_circle_radius = 1000
      # tf_circle_radius = 2000
      
      target_circle_radius = max(500, 150 / (2*pi/nrow(target_nodes)))
      tf_circle_radius = max(1000, 1.9 * target_circle_radius)
      
      
      target_nodes$x = target_circle_radius*cos(seq(0, 2*pi, by = 2*pi/nrow(target_nodes)))[-1]
      target_nodes$y = target_circle_radius*sin(seq(0, 2*pi, by = 2*pi/nrow(target_nodes)))[-1]
      # target_nodes$hidden = TRUE
      
      tf_nodes$x = tf_circle_radius*cos(seq(0, 2*pi, by = 2*pi/nrow(tf_nodes)))[-1]
      tf_nodes$y = tf_circle_radius*sin(seq(0, 2*pi, by = 2*pi/nrow(tf_nodes)))[-1]
      
      # if (length(tf_nodes) > length(target_nodes)) {
      #   
      #   
      # }
      
      # print(target_nodes)
      
      # vis.nodes <- nodes
      # print(dim(rbind(target_nodes, tf_nodes)))
      vis.nodes <- rbind(target_nodes, tf_nodes)
      vis.links <- links
      
      
      
      # visNetwork(vis.nodes,vis.links, width="100%", height="800px") %>%
      #   visIgraphLayout(layout = "layout_in_circle") %>%
      #   # visNodes(physics = TRUE) %>% 
      #   visClusteringByGroup(groups = c('Target', 'TF')) %>%
      #   visOptions(highlightNearest = list(enabled = TRUE, 
      #                                      hover = TRUE, hideColor = 'rgba(200,200,200,200)'))
      
      
      
      visNetwork(vis.nodes, vis.links) %>%
        visGroups(groupname = "Target", color = "#EF767A") %>%
        visGroups(groupname = "TF", color = "#2364AA") %>%
        visNodes(fixed = TRUE) %>%
        # visIgraphLayout(layout = "layout_in_circle") %>%
        visOptions(highlightNearest = list(enabled = TRUE,
                                           hover = TRUE, hideColor = 'rgba(200,200,200,200)')) %>%
        # visEdges(arrows = 'to') %>%
        visLegend(position = 'right', width = 0.1)
      
    })
  }
  
  
  observeEvent(input$searchButton, {
    # print("Search")
    rv$result = get_data()
    rv$selected_result = rv$result
    render_page()
  })
  
  observeEvent(input$checkbox, {
    
    if (length(input$checkbox) > 0) {
      select_target_genes <- strsplit(input$checkbox, " ")
    } else {
      select_target_genes = c()
    }
    rv$selected_result = rv$result[rv$result$target %in% select_target_genes,]
  }, ignoreNULL= F)
  
  observeEvent(input$deselect_all, {
    updateCheckboxGroupInput(session, "checkbox", selected = character(0))
  })
  
  output$cell_main <- renderUI({
    selectInput(inputId="choose_main",
                label="Select Tissue", 
                choices = unique(cell_main_types$tissue))
  })
  
  output$glycopath <- renderUI({
    selectInput(inputId="choose_path",
                label="Select Group", 
                choices = colnames(glycoEnzOnto))
  })
  
}


# TODO:
## config csv
## Readme
## reset view
## Hover Labels  on nodes as well as connections
## Cell types included
## 1. Check if names are found
## % individual percentile per cell type ?
## make the tags xsl, csv
## Loading
## message - no of genes found out of 
## https://excelquick.com/r-shiny/selectinput-dependent-on-another-input/
## Documentation and Report
## node slider - target nodes are not removed 
## create a cell_types table with foregn key on insert script
## UB icon
## 2 Sliders based on p value and frequency
## combination rule - min, max, mean 
## showing 1000 (Max) Genes of n in graph
## Buietify network
## All tissues
## All for each celltypes
## Msg None/empty for all genes
## Prefill examples
## None and all dropdown
## Show all target nodes with no links


## Questions
## Cell Type implimentaion ?
## Select TF Nodes or Target Nodes not required


# ## To install the package from Bioconductor
# if (!requireNamespace("BiocManager", quietly = TRUE))
#   install.packages("BiocManager")
# 
# BiocManager::install("dorothea")
# 
# ## To install the development version from the Github repo:
# devtools::install_github("saezlab/dorothea")
# 
# library(dorothea)
# library(ggplot2)
# library(dplyr)
# 
# net <- dorothea::entire_database
# head(net)
# entire <- dorothea::entire_database
# head(entire)
