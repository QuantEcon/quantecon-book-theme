import plotly.io as pio
import plotly.express as px
import plotly.offline as py

pio.renderers.default = "notebook"

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size="sepal_length")
fig