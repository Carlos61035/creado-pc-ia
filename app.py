import flet as ft
from google import genai
import os
# 🔑 Tu clave de API de Google Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def main(page: ft.Page):
    page.title = "Creador de PC con IA"
    page.theme_mode = ft.ThemeMode.DARK  # Modo oscuro automático
    page.scroll = "adaptive"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Elementos de la interfaz
    titulo = ft.Text("Configurador de PC Inteligente", size=28, weight=ft.FontWeight.BOLD, color="blue400")
    
    input_cpu = ft.TextField(
        label="Escribe el procesador (Ej: Ryzen 5 3600, i7 8700k)", 
        width=400,
        border_color="blue400"
    )
    
    dropdown_presupuesto = ft.Dropdown(
        label="Presupuesto",
        width=400,
        options=[
            ft.dropdown.Option("barato"),
            ft.dropdown.Option("medio"),
            ft.dropdown.Option("mejor"),
        ],
        border_color="blue400"
    )
    
    txt_resultado = ft.Text(size=16, selectable=True)
    
    # Barra de progreso para cuando la IA está pensando
    progreso = ft.ProgressBar(width=400, visible=False)

    def btn_click(e):
        if not input_cpu.value or not dropdown_presupuesto.value:
            txt_resultado.value = "⚠️ Por favor, llena ambos campos."
            page.update()
            return
        
        # Mostrar animación de carga
        progreso.visible = True
        txt_resultado.value = "🤖 Consultando a la IA de Google... Por favor espera..."
        page.update()

        prompt = f"""
        Actúa como un ingeniero experto en hardware de PC.
        El usuario tiene o quiere el procesador: "{input_cpu.value}".
        Calcula una configuración óptima enfocada en el presupuesto: "{dropdown_presupuesto.value}".
        Evita cuellos de botella severos considerando el año del procesador.
        
        Devuelve la respuesta limpia:
        • Tarjeta Gráfica: [Modelo]
        • Memoria RAM: [Cantidad y tipo]
        • Fuente de Poder: [Watts y certificación]
        • Nota del Ingeniero: [Explicación breve]
        """

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            txt_resultado.value = response.text
        except Exception as ex:
            txt_resultado.value = f"❌ Error: {ex}"
        
        # Ocultar animación de carga
        progreso.visible = False
        page.update()

    btn_calcular = ft.ElevatedButton("Calcular Configuración", on_click=btn_click, bgcolor="blue400", color="white")

    # Agregar todo a la pantalla
    page.add(
        titulo,
        ft.Text("Soporta cualquier procesador desde 2018 hasta la actualidad", size=14, color="grey400"),
        ft.Divider(height=20, color="transparent"),
        input_cpu,
        dropdown_presupuesto,
        btn_calcular,
        progreso,
        ft.Divider(height=20),
        ft.Container(content=txt_resultado, width=450, padding=10, border_radius=10, bgcolor="surfaceVariant")
    )

ft.app(target=main, port=8000, view=ft.AppView.WEB_BROWSER)