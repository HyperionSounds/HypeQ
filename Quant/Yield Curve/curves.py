import matplotlib.pyplot as plt
import pandas as pd
import quandl as ql

yield_ = ql.get("USTREASURY/YIELD")

today = yield_.iloc[-1,:]
month_ago = yield_.iloc[-30,:]
print("today: ",today)

df = pd.concat([today, month_ago], axis=1)
df.columns = ['today', 'month_ago']

df.plot(style={'today': 'ro-', 'month_ago': 'bx--'}
        ,title='Treasury Yield Curve, %');

print(df)

plt.show()