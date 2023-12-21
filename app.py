from flask import Flask, render_template, jsonify, redirect, url_for

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from data.data import delitos_tipo_py, del_tip_2013, delitos_tipo_pt, corr_delit, gender_2018, gender_2019, gender_2020, gender_2021

app = Flask(__name__)

@app.route('/')
def index_redirect():
    return redirect(url_for("index"))

@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/myprojects')
def myproyects():

    return render_template('myprojects.html')

@app.route('/EDA')
def eda():

    # Crear la gráfica
    fig0 = go.Figure()
    fig0.add_trace(go.Bar(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Total"], name="Total", marker_color="#5594B0"))
    fig0.add_trace(go.Scatter(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Total"], name="Total", mode="lines", line=dict(color="orange", dash="dash")))

    # Personalizar el diseño de la gráfica
    fig0.update_layout(title="Delitos totales por año", xaxis_title="Periodo", yaxis_title="Total", showlegend=False, template="plotly_dark", autosize=True)
    for i, row in delitos_tipo_py.iterrows():
        fig0.add_annotation(x=row["Periodo"], y=row["Total"], text=str(int(row["Total"])), showarrow=False, font=dict(size=14))

    # Mostrar la gráfica
    plot_div_eda_0 = fig0.to_html(full_html=False)

    # Crear la figura
    fig3 = go.Figure()

    colores_delitos = {
    "Contra la intimidad, derecho a la propia imagen": "#1f77b4",
    "Contra el honor": "#ff7f0e",
    "Contra las relaciones familiares": "#2ca02c",
    "Contra el patrimonio y el orden socioeconómico": "#d62728",
    "Contra la Hacienda Pública y Seguridad Social": "#9467bd",
    "Contra los derechos de los ciudadanos extranjeros": "#8c564b",
    "Contra los derechos de los trabajadores": "#e377c2",
    "Ordenación del territorio, urbanismo, protección del patrimonio histórico y medio ambiente": "#9fd4e5",
    "Contra la seguridad colectiva": "#bcbd22",
    "Falsedades": "#17becf",
    "Contra la Administración Pública": "#ff9896",
    "Contra la Administración de Justicia": "#dbdb8d",
    "Contra la Constitución": "#9edae5",
    "Contra el orden público": "#aec7e8",
    "Traición, contra la paz y defensa nacional": "#c5b0d5",
    "Contra la Comunidad Internacional": "#f7b6d2",
    "Homicidio y sus formas": "#1f77b4",
    "Aborto": "#ff7f0e",
    "Lesiones": "#2ca02c",
    "Lesiones al feto": "#d62728",
    "Manipulación genética": "#9467bd",
    "Contra la libertad": "#8c564b",
    "Trata de seres humanos": "#e377c2",
    "Torturas e integridad moral": "#7f7f7f",
    "Contra la libertad e indemnidad sexuales": "#bcbd22",
    "Omisión del deber de socorro": "#17becf"
}

    # Agregar las barras correspondientes a cada tipo de delito

    # for i, nv2 in enumerate(del_tip_2013["Nv2"].unique()):
    #     subset = del_tip_2013[del_tip_2013["Nv2"] == nv2]
    #     color = colores_delitos[nv2]
    #     fig3.add_trace(go.Bar(x=[nv2], y=[subset["Total"].iloc[0]], name=nv2, marker_color=color))

    # Leyenda sin texto
    for i, nv2 in enumerate(del_tip_2013["Nv2"].unique()):
        subset = del_tip_2013[del_tip_2013["Nv2"] == nv2]
        color = colores_delitos[nv2]
        fig3.add_trace(go.Bar(x=[nv2], y=[subset["Total"].iloc[0]], name="", marker_color=color))

    # Personalizar el diseño de la gráfica
    fig3.update_layout(title="Total de Delitos por Tipo en 2013", yaxis_title="Total", template="plotly_dark", autosize=True, showlegend=True)

    # Actualizar los colores de la leyenda
    # for i, trace in enumerate(fig3.data):
    #     nv2 = trace.name
    #     color = colores_delitos[nv2]
    #     fig3.data[i].marker.color = color

    # Actualizar los colores de la leyenda
    for i, trace in enumerate(fig3.data):
        nv2 = trace.marker.color
        fig3.data[i].marker.color = nv2

    fig3.update_xaxes(tickmode="array", tickvals=[])
    # Mostrar la gráfica
    plot_div_eda_3 = fig3.to_html(full_html=False)

    # Incremento absoluto
    fig1 = go.Figure()

    fig1.add_trace(go.Bar(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Incremento"], name="Incremento"))
    fig1.add_trace(go.Scatter(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Incremento"], name="Total", line=dict(color='orange', dash='dash')))

    fig1.update_layout(title_text="Incremento absoluto anual", xaxis_title="Periodo", yaxis_title="Incremento", template="plotly_dark", autosize=True)
    for i, row in delitos_tipo_py.iterrows():
        fig1.add_annotation(x=row["Periodo"], y=row["Incremento"], text=str(int(row["Incremento"])), showarrow=False, font=dict(size=14))

    plot_div_eda_1 = fig1.to_html(full_html=False)

    # Incremento relativo
    fig2 = go.Figure()

    fig2.add_trace(go.Bar(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Incremento%"], name="Incremento%"))
    fig2.add_trace(go.Scatter(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Incremento%"], name="Total", line=dict(color='orange', dash='dash')))

    fig2.update_layout(title_text="Incremento porcentual anual", xaxis_title="Periodo", yaxis_title="Incremento%", template="plotly_dark", autosize=True)
    for i, row in delitos_tipo_py.iterrows():
        fig2.add_annotation(x=row["Periodo"], y=row["Incremento%"], text=f"{row['Incremento%']:.2f}%", showarrow=False, font=dict(size=14))

    plot_div_eda_2 = fig2.to_html(full_html=False)

    fig4 = px.bar(delitos_tipo_pt,x="Nv2",y="Total",hover_data="Periodo",color="Periodo",opacity=0.6, 
             color_discrete_map={2013:"#1f77b4", 2014:"#ff7f0e", 2015:"#2ca02c", 2016:"#d62728", 2017:"#9467bd", 2018:"#8c564b", 2019:"#e377c2", 2020:"#7f7f7f",2021:"#bcbd22"},
             category_orders={"Periodo": [2013,2014,2015,2016,2017,2018,2019,2020,2021]})
    fig4.update_layout(title='Delitos por tipo y año',
                    xaxis_title='Delitos',
                    yaxis_title='Total',
                    legend_title='Tipo de delito', template="plotly_dark", autosize=True, barmode="overlay")
    fig4.update_xaxes(tickmode="array", tickvals=[])
    # fig4.update_yaxes(tickmode="array", tickvals=[])
    plot_div_eda_4 = fig4.to_html(full_html=False)

    #REVISAR ESTO
    # delitos_tipo_pt_f = delitos_tipo_pt[delitos_tipo_pt['Periodo'] != 2013]
    # fig5 = px.line(delitos_tipo_pt_f, x='Periodo', y='Incremento', color='Nv2')

    # fig5.update_layout(title='Incremento anual de delitos por tipo',
    #                 xaxis_title='Año',
    #                 yaxis_title='Incremento',
    #                 legend_title='Tipo de delito', template="plotly_dark", width=1500, height=800)

    # plot_div_eda_5 = fig5.to_html(full_html=False)

    # Heatmap a partir de la matriz de correlación 

    fig6 = px.imshow(corr_delit, text_auto=True, aspect="auto", color_continuous_scale="Jet")
    fig6.update_layout(template="plotly_dark", autosize=True)
    # fig.update_xaxes(tickmode="array", tickvals=[])
    # fig6.update_yaxes(tickfont=dict(size=10))
    fig6.update_xaxes(tickmode="array", tickvals=[])
    fig6.update_yaxes(tickmode="array", tickvals=[])

    plot_div_eda_6 = fig6.to_html(full_html=False)

    # Matriz de correlación 2

    corr_delit_2 = corr_delit[(corr_delit < -0.5) | (corr_delit > 0.5)]

    # Heatmap a partir de la matriz de correlación 2

    fig7 = px.imshow(corr_delit_2, text_auto=True, aspect="auto", color_continuous_scale="Jet")
    fig7.update_layout(template="plotly_dark", autosize=True)
    # fig.update_xaxes(tickmode="array", tickvals=[])
    # fig7.update_yaxes(tickfont=dict(size=10))
    fig7.update_xaxes(tickmode="array", tickvals=[])
    fig7.update_yaxes(tickmode="array", tickvals=[])

    plot_div_eda_7 = fig7.to_html(full_html=False)

    fig8 = go.Figure()
    fig8.add_trace(go.Bar(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Tasa_Crim"], name="Total", marker_color="#5594B0"))
    fig8.add_trace(go.Scatter(x=delitos_tipo_py["Periodo"], y=delitos_tipo_py["Tasa_Crim"], name="Total", mode="lines", line=dict(color="orange", dash="dash")))

    fig8.update_layout(title="Variación de la Tasa de criminalidad", 
                    xaxis_title="Periodo", yaxis_title="Total",
                    showlegend=False, template="plotly_dark", 
                    autosize=True)

    for i, row in delitos_tipo_py.iterrows():
        fig8.add_annotation(x=row["Periodo"], y=row["Tasa_Crim"], text=f"{row['Tasa_Crim']:.2f}", showarrow=False, font=dict(size=14))

    plot_div_eda_8 = fig8.to_html(full_html=False)

    from plotly.subplots import make_subplots

    specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]
    fig9 = make_subplots(rows=2, cols=2, specs=specs, subplot_titles=['2021', '2020', '2019', '2018'])
    fig9.add_trace(go.Pie(labels = gender_2021["Sexo"],values=gender_2021["Total"], pull=[0.05, 0.05, 0.05],name="2021"), 1, 1)
    fig9.add_trace(go.Pie(labels = gender_2020["Sexo"],values=gender_2020["Total"], pull=[0.05, 0.05, 0.05],name="2020"), 1, 2)
    fig9.add_trace(go.Pie(labels = gender_2019["Sexo"],values=gender_2019["Total"], pull=[0.05, 0.05, 0.05],name="2019"), 2, 1)
    fig9.add_trace(go.Pie(labels = gender_2018["Sexo"],values=gender_2018["Total"], pull=[0.05, 0.05, 0.05],name="2018"), 2, 2)

    fig9.update_traces(textposition='inside', textinfo='percent+label')
    fig9.update_layout(title="Condenados por género 2018-2021", 
                    showlegend=True, template="plotly_dark", 
                    autosize=True)
    plot_div_eda_9 = fig9.to_html(full_html=False)


    return render_template('eda.html', plot_div=[plot_div_eda_0,plot_div_eda_1,plot_div_eda_2, plot_div_eda_3, plot_div_eda_4, plot_div_eda_6, plot_div_eda_7, plot_div_eda_8, plot_div_eda_9])

@app.route('/MLproyect')
def MLproyect():

    return render_template('MLproyect.html')

@app.route('/techs')
def techs():
    return render_template('techs.html')

@app.route('/aboutme')
def aboutMe():


    return render_template('aboutme.html')

if __name__ == '__main__':
    app.run(debug=True)
