import dash_html_components as html
import dash_core_components as dcc


def get_app_layout(
    heatmap,
    polar_bar_chart_winter,
    polar_bar_chart_spring,
    polar_bar_chart_summer,
    polar_bar_chart_fall,
    map,
    temperature_scatter_plot,
    snow_scatter_plot,
    rain_scatter_plot
):

    figure_config = dict(
        showTips=False,
        showAxisDragHandles=False,
        displayModeBar=False,
        dragMode=False
    )

    return html.Div(className='content', children=[
        html.Main(className='page-container', children=[
            html.Div(
                className="shortcuts",
                children=[
                    html.Span("Sections"),
                    html.Ul(children=[
                        html.Li(children=[
                            html.A("Évolution temporelle des passages à vélo de 2019 à 2023",
                                href="#temporal-evolution")
                        ]),
                        html.Li(children=[
                            html.A("Nombre de passages à vélo horaire par saison",
                                href="#hourly-traffic")
                        ]),
                        html.Li(children=[
                            html.A("Achalandage des pistes cyclables",
                                href="#bike-paths-traffic")
                        ]),
                        html.Li(children=[
                            html.A("Impact des conditions météorologiques",
                                href="#weather-condition"),
                            html.Ul(children=[
                                html.Li(children=[
                                    html.A("Influence de la température",
                                           href="#temperature")
                                ]),
                                html.Li(children=[
                                    html.A("Influence de la quantité de neige tombée",
                                           href="#snow")
                                ]),
                                html.Li(children=[
                                    html.A("Influence de la quantité de pluie tombée",
                                           href="#rain")
                                ])
                            ])
                        ]),
                    ])
                ]
            ),


            html.H1(
                "Le vélo à Montréal : Évolution des pistes cyclables et tendances d'utilisation"
            ),
            html.B(
                "Par : Émile Watier, Gabriel Billard, Jonathan Tapiero, Lana Pham, Nargisse Benbiga, Thomas Logeais"),
            html.P(
                "Au fil des années, le vélo s'est imposé comme un élément essentiel du paysage urbain de Montréal. \
                Son évolution, marquée par le développement des pistes cyclables et les changements dans les habitudes de déplacement, \
                témoigne de l'émergence d'un mode de vie plus durable et actif dans la ville. Pour en savoir plus sur cet aspect, \
                nous nous appuierons sur les données ouvertes fournies par la ville de Montréal entre 2019 et 2023 afin de mieux \
                comprendre l'évolution temporelle et géographique de cette tendance ainsi que les variables qui y contribuent.",
                className="introduction"
            ),


            html.H2(
                children="Évolution temporelle des passages à vélo de 2019 à 2023",
                id="temporal-evolution"
            ),
            html.P("Cette section aborde l'évolution de l'achalandage des pistes \
                cyclables de janvier 2019 à janvier 2024."),
            dcc.Graph(
                figure=heatmap,
                id='heatmap',
                config=figure_config
            ),
            html.P("Une diminution drastique de l'achalandage des pistes \
                cyclables est observée lors des périodes hivernales, à savoir de \
                novembre à mars en raison des défis liés aux conditions \
                météorologiques et la présence de neige et verglas sur les routes. \
                De plus, le service de vélos en libre-service Bixi de Montréal \
                n'est pas opérationnel durant cette période, ce qui contribue \
                également à cette diminution d'achalandage. Nous pouvons ainsi \
                conclure que l'hiver invite les citoyens à se déplacer d'une autre \
                manière qu'à vélo."),
            html.P("Cependant, avec l'arrivée du printemps, les pistes \
                cyclables voient une augmentation notable de leur fréquentation. Ce\
                regain d'intérêt pour le vélo se maintient tout au long de la \
                saison estivale, ce qui suggère que les conditions météorologiques \
                plus clémentes incitent un nombre croissant de personnes à opter \
                pour ce mode de transport."),
            html.P("Nous constatons également qu'au fil des années, \
                l'achalandage annuel a augmenté de manière graduelle. L'année 2022 \
                présente le plus fort achalandage, comparativement aux autres \
                années. De plus, selon Valérie Plante, la mairesse de Montréal, \
                les déplacements à vélo connaissent une hausse de 20%% entre 2020 \
                et 2021"),


            html.H2(
                children="Nombre de passages à vélo horaire par saison",
                id="hourly-traffic",
            ),
            html.P(
                "Cette section aborde l'achalandage moyen des pistes cyclables \
                    par heure des quatre saisons."),
            html.Div(className='polar-bar-charts-container', children=[
                dcc.Graph(
                    figure=polar_bar_chart_winter,
                    config=figure_config
                ),
                dcc.Graph(
                    figure=polar_bar_chart_spring,
                    config=figure_config
                ),
                dcc.Graph(
                    figure=polar_bar_chart_summer,
                    config=figure_config
                ),
                dcc.Graph(
                    figure=polar_bar_chart_fall,
                    config=figure_config
                ),
            ]),

            html.P("En observant ces horloges de l'achalandage, un motif \
                se dessine clairement : les pics d'activité coïncident avec les \
                heures de début et de fin de journée de travail, soulignant 8 \
                heures et 17 heures comme moments privilégiés du flux cycliste. \
                L'été, nous observons que l’achalandage se prolonge plus loin dans \
                la journée, alors qu'en hiver, l'obscurité invite à ranger les \
                vélos plus tôt. Nous constatons également que les passages à vélo \
                sont plus nombreux l'après-midi."),


            html.H2(
                children="Achalandage des pistes cyclables",
                id="bike-paths-traffic"
            ),
            html.P("Cette section aborde l'achalandage des pistes cyclables ainsi \
                que des compteurs à vélo à Montréal. Chaque compteur est représenté\
                par un cercle et sa taille varie selon le nombre de passages, \
                alors que la couleur change selon l'année à laquelle un compteur est\
                implanté. Les pistes cyclables sont représentées par les traits \
                verts sur la carte."),
            dcc.Graph(
                figure=map,
                id='map',
                config=figure_config
            ),
            html.P("Une présence accrue des compteurs de vélo ainsi que \
                des pistes cyclables est constatée dans les environs de \
                l'arrondissement du Plateau Mont-Royal, soulignant ainsi une forte \
                utilisation du vélo comme mode de transport.  Cependant, plusieurs \
                pistes cyclables sont présentes en dehors de ces environs avec une \
                faible quantité de compteurs, voire même une quantité nulle. \
                L'achalandage de ces pistes cyclables ne peut ainsi être mesuré de \
                manière représentative."),
            html.P("Une grande majorité des compteurs à vélo ont été \
                implantés en 2019 ou avant. Quelques-uns ont été implantés depuis."),


            html.H2(
                children="Impact des conditions météorologiques",
                id="weather-condition"
            ),
            html.P("Cette section aborde l'influence de diverses conditions \
                météorologiques sur le nombre de passages à vélo à Montréal. Il est \
                à noter que la visualisation prend seulement en compte les compteurs\
                communs entre les années afin de ne pas considérer l'évolution du \
                nombre de compteurs."),

            html.H3(
                children="Influence de la température",
                id="temperature"
            ),
            dcc.Graph(
                figure=temperature_scatter_plot,
                id='temperature-scatter-plot',
                config=figure_config
            ),
            html.P("Il est évident que la température moyenne a une grande \
                incidence sur les passages à vélo. En effet, nous pouvons constater \
                qu'à des températures négatives, c'est-à-dire inférieures à 0°C, le \
                nombre de passages est faible et varie peu de jour en jour. Cela \
                met également en évidence l'influence des périodes hivernales, où il\
                fait plus froid à l'extérieur, sur les passages à vélo à Montréal."),
            html.P("En ce qui a trait aux températures positives, à savoir \
                supérieures à 0°C, nous pouvons observer que le nombre de passages \
                à vélo est plus élevé comparativement aux températures froides. De \
                plus, les passages varient davantage et fluctuent de plusieurs \
                dizaines de milliers de passages. Ces variations indiquent que, \
                pour les températures plus chaudes, les passages sont influencés \
                par d'autres facteurs tels que la quantité de neige ou la quantité \
                de pluie, en plus de la température extérieure."),

            html.H3(
                "Influence de la quantité de neige tombée",
                id="snow"
            ),
            dcc.Graph(
                figure=snow_scatter_plot,
                id='snow-scatter-plot',
                config=figure_config
            ),
            html.P("La moyenne des passages à vélo lorsqu'aucune neige ne tombe \
                (représentée par le trait pointillé horizontal gris) est de \
                31 445,05 passages. Comparativement à ce nombre, la grande majorité\
                des journées présentent un faible achalandage lorsqu'il neige à \
                Montréal, indiquant ainsi la forte influence que la neige tombante \
                a sur l'achalandage sur les pistes cyclables. En effet, la présence \
                de neige tombante invite les citoyens à ranger leurs vélos et à \
                opter pour un autre moyen de transport."),
            html.P("Toutefois, deux exceptions se présentent : le mercredi 6 \
                novembre 2019 ainsi que le mardi 7 février 2023. À ces dates, de \
                forts achalandages de 35 573 passages avec 1,4 cm de neige et de \
                33 927 passages avec 2,2 cm de neige respectivement se manifestent."),
            html.P("Tout d'abord, concernant la journée du mercredi 6 novembre \
                2019, aucun événement particulier à Montréal pouvant justifier une \
                grande fréquentation des voies cyclables n'a eu lieu. Une \
                température moyenne de 2,7°C est observée, ce qui correspond à une \
                température assez commune lors du mois de novembre. Le temps \
                ensoleillé lors de cette journée pourrait cependant expliquer une \
                importante fréquentation des pistes cyclables."),
            html.P("Ensuite, en 2023, le festival de musique électronique Igloofest\
                a eu lieu du 19 janvier au 11 février. Cet événement pourrait \
                justifier un fort achalandage des voies cyclables lors du mardi 7 \
                février, malgré une présence de 2,2 cm de neige. Néanmoins, il est \
                à noter qu'une température moyenne de -7,6°C est observée au \
                courant de cette journée, avec une température minimale de -16,9°C,\
                ce qui est assez froid."),
            html.P("En dépit de ces deux points aberrants, étant donné que la \
                grande majorité des journées ayant de la neige présente une \
                fréquentation des pistes cyclables sous la moyenne lorsqu'il n'y a \
                aucune neige tombante, nous pouvons conclure que la neige tombante \
                a une forte influence sur le nombre de passages à vélo à Montréal."),

            html.H3(
                "Influence de la quantité de pluie tombée",
                id="rain"
            ),
            dcc.Graph(
                figure=rain_scatter_plot,
                id='rain-scatter-plot',
                config=figure_config
            ),
            html.P("La moyenne des passages à vélo lorsqu'aucune neige ne tombe est\
                de 28 586,44 passages. Elle est représentée dans le graphique par \
                le trait pointillé horizontal. Contrairement à l'influence qu'a la \
                neige sur les passages à vélo, la quantité de pluie détient un plus\
                faible impact sur les passages à vélo. En effet, une faible \
                quantité de pluie tombante ne semble pas influencer les passages à \
                vélo, étant donné une forte variation du nombre de passages à vélo \
                en présence de peu de pluie."),
            html.P("Cependant, plus il y a de la pluie, moins les journées à fort \
                achalandage sont nombreuses. Par conséquent, moins les pistes \
                cyclables sont achalandées. Cela indique ainsi un plus fort impact \
                dans le cas où la quantité de pluie est plus élevée. Effectivement, \
                lorsqu'au moins 34 mm de pluie est atteint, le nombre de passages \
                est en dessous de la fréquence moyenne des pistes cyclables moyenne \
                sans aucune pluie. Une exception se présente le mercredi 22 juin \
                2022 : il y a eu 46 586 passages avec 38 mm de pluie. Bien qu'aucun \
                événement particulier pouvant justifier ce fort achalandage se \
                présente cette journée, une température moyenne assez chaude de \
                19,6°C est observée."),
        ])
    ])
