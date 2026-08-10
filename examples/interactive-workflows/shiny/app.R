library(shiny)

ui <- fluidPage(
  titlePanel("RCC Shiny example"),
  sliderInput("n", "Number of observations", 10, 1000, 100),
  plotOutput("histogram")
)

server <- function(input, output, session) {
  output$histogram <- renderPlot(hist(rnorm(input$n)))
}

shinyApp(ui, server)
