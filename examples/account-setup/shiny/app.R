library(shiny)

ui <- fluidPage(
  titlePanel("RCC Shiny starter"),
  sidebarLayout(
    sidebarPanel(sliderInput("bins", "Histogram bins", min = 5, max = 50, value = 20)),
    mainPanel(plotOutput("histogram"))
  )
)

server <- function(input, output, session) {
  output$histogram <- renderPlot({
    hist(faithful$eruptions, breaks = input$bins, col = "#0a8fb2", border = "white")
  })
}

shinyApp(ui, server)
