# ── Libraries ─────────────────────────────────────────────────
options(timeout = 300)
options(repos = c(CRAN = "https://cloud.r-project.org"))

packages <- c("shiny", "shinydashboard", "plotly", "DT", "tidyverse", "scales")
for (pkg in packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    cat("📦 Installing:", pkg, "\n")
    install.packages(pkg, type = "binary")
  } else {
    cat("✅ Already installed:", pkg, "\n")
  }
}

library(shiny)
library(shinydashboard)
library(plotly)
library(DT)
library(tidyverse)
library(scales)

# ── Load Data ─────────────────────────────────────────────────
df <- read_csv("../../data/processed/superstore_clean.csv") %>%
  mutate(
    Order.Date    = as.Date(`Order Date`, format = "%Y-%m-%d"),
    Segment       = as.factor(Segment),
    Region        = as.factor(Region),
    Category      = as.factor(Category),
    `Ship Mode`   = as.factor(`Ship Mode`),
    `Profit Tier` = as.factor(`Profit Tier`)
  )

# ══════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════
ui <- dashboardPage(
  skin = "blue",
  
  # ── Header ────────────────────────────────────────────────
  dashboardHeader(title = "Superstore Analytics"),
  
  # ── Sidebar ───────────────────────────────────────────────
  dashboardSidebar(
    sidebarMenu(
      menuItem("Overview",      tabName = "overview", icon = icon("chart-bar")),
      menuItem("Profitability", tabName = "profit",   icon = icon("dollar-sign")),
      menuItem("Data Table",    tabName = "table",    icon = icon("table"))
    ),
    hr(),
    
    # Global Filters — apply to all tabs
    selectInput("segment", "Customer Segment:",
                choices  = c("All", levels(df$Segment)),
                selected = "All"),
    
    selectInput("region", "Region:",
                choices  = c("All", levels(df$Region)),
                selected = "All"),
    
    selectInput("category", "Category:",
                choices  = c("All", levels(df$Category)),
                selected = "All"),
    
    sliderInput("discount", "Discount Range:",
                min   = 0, max = 0.8,
                value = c(0, 0.8), step = 0.05)
  ),
  
  # ── Body ──────────────────────────────────────────────────
  dashboardBody(
    tabItems(
      
      # ── Tab 1: Overview ───────────────────────────────────
      tabItem(tabName = "overview",
              
              # KPI Boxes
              fluidRow(
                valueBoxOutput("box_orders",  width = 4),
                valueBoxOutput("box_sales",   width = 4),
                valueBoxOutput("box_profit",  width = 4)
              ),
              
              # Charts Row 1
              fluidRow(
                box(title = "Monthly Sales Trend",    width = 8, plotlyOutput("plot_trend",    height = 300)),
                box(title = "Sales by Category",      width = 4, plotlyOutput("plot_category", height = 300))
              ),
              
              # Charts Row 2
              fluidRow(
                box(title = "Sales by Region and Segment", width = 12, plotlyOutput("plot_segment", height = 300))
              )
      ),
      
      # ── Tab 2: Profitability ──────────────────────────────
      tabItem(tabName = "profit",
              
              fluidRow(
                box(title = "Discount vs Profit Margin %",    width = 6, plotlyOutput("plot_scatter", height = 350)),
                box(title = "Profit Distribution by Region",  width = 6, plotlyOutput("plot_box",     height = 350))
              ),
              
              fluidRow(
                box(title = "Profit Tier Distribution",          width = 5, plotlyOutput("plot_tier",   height = 300)),
                box(title = "Top 10 Sub-Categories by Profit",   width = 7, plotlyOutput("plot_subcat", height = 300))
              )
      ),
      
      # ── Tab 3: Data Table ─────────────────────────────────
      tabItem(tabName = "table",
              box(title = "Filtered Dataset", width = 12, DTOutput("data_table"))
      )
    )
  )
)

# ══════════════════════════════════════════════════════════════
# SERVER
# ══════════════════════════════════════════════════════════════
server <- function(input, output, session) {
  
  # ── Reactive filtered dataset ────────────────────────────
  # Recalculates automatically whenever any filter changes
  filtered <- reactive({
    d <- df
    if (input$segment  != "All") d <- d %>% filter(Segment  == input$segment)
    if (input$region   != "All") d <- d %>% filter(Region   == input$region)
    if (input$category != "All") d <- d %>% filter(Category == input$category)
    d <- d %>% filter(Discount >= input$discount[1],
                      Discount <= input$discount[2])
    d
  })
  
  # ── KPI: Total Orders ─────────────────────────────────────
  output$box_orders <- renderValueBox({
    valueBox(
      format(nrow(filtered()), big.mark = ","),
      "Total Orders",
      icon  = icon("shopping-cart"),
      color = "blue"
    )
  })
  
  # ── KPI: Total Sales ──────────────────────────────────────
  output$box_sales <- renderValueBox({
    valueBox(
      dollar(sum(filtered()$Sales, na.rm = TRUE), scale = 0.001, suffix = "K"),
      "Total Sales",
      icon  = icon("chart-line"),
      color = "green"
    )
  })
  
  # ── KPI: Total Profit ─────────────────────────────────────
  output$box_profit <- renderValueBox({
    val <- sum(filtered()$Profit, na.rm = TRUE)
    valueBox(
      dollar(val, scale = 0.001, suffix = "K"),
      "Total Profit",
      icon  = icon("dollar-sign"),
      color = if (val >= 0) "yellow" else "red"
    )
  })
  
  # ── Plot 1: Monthly Sales Trend ───────────────────────────
  output$plot_trend <- renderPlotly({
    trend <- filtered() %>%
      mutate(YM = floor_date(Order.Date, "month")) %>%
      group_by(YM) %>%
      summarise(Sales = sum(Sales, na.rm = TRUE), .groups = "drop")
    
    plot_ly(trend, x = ~YM, y = ~Sales,
            type = "scatter", mode = "lines",
            line = list(color = "#4e79a7", width = 2)) %>%
      layout(
        xaxis = list(title = ""),
        yaxis = list(title = "Sales (USD)"),
        hovermode = "x unified"
      )
  })
  
  # ── Plot 2: Sales by Category ─────────────────────────────
  output$plot_category <- renderPlotly({
    cat_data <- filtered() %>%
      group_by(Category) %>%
      summarise(Sales = sum(Sales, na.rm = TRUE), .groups = "drop")
    
    plot_ly(cat_data,
            x = ~Sales,
            y = ~reorder(Category, Sales),
            type = "bar",
            orientation = "h",
            marker = list(color = c("#4e79a7", "#f28e2b", "#59a14f"))) %>%
      layout(
        xaxis = list(title = "Sales (USD)"),
        yaxis = list(title = "")
      )
  })
  
  # ── Plot 3: Sales by Region and Segment ──────────────────
  output$plot_segment <- renderPlotly({
    seg_data <- filtered() %>%
      group_by(Region, Segment) %>%
      summarise(Sales = sum(Sales, na.rm = TRUE), .groups = "drop")
    
    plot_ly(seg_data,
            x      = ~Region,
            y      = ~Sales,
            color  = ~Segment,
            colors = c("Consumer"    = "#4e79a7",
                       "Corporate"   = "#59a14f",
                       "Home Office" = "#f28e2b"),
            type   = "bar",
            barmode = "group") %>%
      layout(
        xaxis = list(title = ""),
        yaxis = list(title = "Sales (USD)")
      )
  })
  
  # ── Plot 4: Discount vs Profit Margin % ──────────────────
  output$plot_scatter <- renderPlotly({
    scatter_data <- filtered() %>%
      filter(`Profit Margin %` > -150)
    
    plot_ly(scatter_data,
            x      = ~Discount,
            y      = ~`Profit Margin %`,
            color  = ~Category,
            colors = c("Furniture"       = "#4e79a7",
                       "Office Supplies" = "#f28e2b",
                       "Technology"      = "#59a14f"),
            type   = "scatter",
            mode   = "markers",
            marker = list(size = 4, opacity = 0.5)) %>%
      layout(
        xaxis = list(title = "Discount", tickformat = ".0%"),
        yaxis = list(title = "Profit Margin %")
      )
  })
  
  # ── Plot 5: Profit Distribution by Region ────────────────
  output$plot_box <- renderPlotly({
    plot_ly(filtered(),
            x      = ~Region,
            y      = ~Profit,
            color  = ~Region,
            colors = c("Central" = "#4e79a7",
                       "East"    = "#59a14f",
                       "South"   = "#f28e2b",
                       "West"    = "#e15759"),
            type   = "box") %>%
      layout(
        xaxis      = list(title = ""),
        yaxis      = list(title = "Profit (USD)"),
        showlegend = FALSE
      )
  })
  
  # ── Plot 6: Profit Tier Donut ─────────────────────────────
  output$plot_tier <- renderPlotly({
    tier <- filtered() %>%
      count(`Profit Tier`)
    
    plot_ly(tier,
            labels = ~`Profit Tier`,
            values = ~n,
            type   = "pie",
            hole   = 0.45) %>%
      layout(showlegend = TRUE)
  })
  
  # ── Plot 7: Top 10 Sub-Categories by Profit ──────────────
  output$plot_subcat <- renderPlotly({
    sub <- filtered() %>%
      group_by(`Sub-Category`) %>%
      summarise(Profit = sum(Profit, na.rm = TRUE), .groups = "drop") %>%
      arrange(desc(Profit)) %>%
      head(10)
    
    plot_ly(sub,
            x           = ~Profit,
            y           = ~reorder(`Sub-Category`, Profit),
            type        = "bar",
            orientation = "h",
            marker      = list(
              color = ifelse(sub$Profit >= 0, "#59a14f", "#e15759")
            )) %>%
      layout(
        xaxis = list(title = "Profit (USD)"),
        yaxis = list(title = "")
      )
  })
  
  # ── Data Table ────────────────────────────────────────────
  output$data_table <- renderDT({
    filtered() %>%
      select(`Order ID`, `Order Date`, Segment, Region,
             Category, `Sub-Category`, Sales, Profit,
             Discount, `Profit Margin %`) %>%
      datatable(
        options = list(pageLength = 15, scrollX = TRUE),
        filter  = "top"
      )
  })
}

# ── Run App ───────────────────────────────────────────────────
shinyApp(ui = ui, server = server)