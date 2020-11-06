import pandas as pd
import plotly.express as px

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
# breakpoint()
df = px.data.gapminder()
fig = px.line(df, x="year", y="lifeExp", color='country')
# breakpoint()
fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp",
	         size="pop", color="continent",
                 hover_name="country", log_x=True, size_max=60)
breakpoint()