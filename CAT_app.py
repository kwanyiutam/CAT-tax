from shiny import App, reactive, render, ui, run_app

## Project modules to input
import gen_input # Modules to check inputs

app_ui = ui.page_fluid(
    ui.input_action_button("generate_input", "Generate Sample Input"), 
    ui.output_table("gen_input_table"),
)

def server(input, output, session):
    @render.table
    @reactive.event(input.generate_input)
    def gen_input_table():
        return gen_input.gen_input_main()

app = App(app_ui, server)