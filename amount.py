from nu_wright_lab_util import regress
import nu_wright_lab_util.sample_stats as ss
import datetime
import pandas as pd
import numpy as np
from hetrobit import hetrobit, stat_by_group_fn

data = pd.read_csv('data.csv')
d = data.query("group in ['A30','A60','A120','A240'] and time > 0").copy()
d['slope2'] = d.slope*2
md = hetrobit('slope2 ~ group:time + pretest','0+group',d,error_prior=5)

print "Model validation:"
print md.validate()
print md.validate([stat_by_group_fn('std',md,lambda x,a: np.var(x,a))])
print "WAIC: %4.0f (SE = %2.0f)" % md.WAIC()[:2]

p = pd.DataFrame(md.df.groupby(['group','time']).pretest.mean()).reset_index()
y = md.predict(p)
entries = p.shape[0]
p = p.iloc[np.repeat(np.arange(entries),y.shape[1]),:]
p['sample'] = np.tile(np.arange(y.shape[1]),entries)
p['y'] = np.reshape(y,y.shape[0]*y.shape[1])
p.set_index(['group', 'time','sample','pretest'],inplace=True)

imp2 = p.reset_index('pretest').query('time == 2').reset_index('time',drop=True)
imp3 = p.reset_index('pretest').query('time == 3').reset_index('time',drop=True)
imp3['imp23'] = imp2.y/2 - imp3.y/2
gimps = imp3.imp23.unstack('group')
print "Improvement from day 2 pre to day 2 post"
print ss.coef_table(gimps,gimps.columns)

imp = p.reset_index('pretest').query('time == 3')
imp['imp'] = imp.y/2 - imp.pretest/2
gimps = imp.imp.unstack('group')
print "Improvement from day 1 pre to day 2 post"
print ss.coef_table(gimps,gimps.columns)
print ss.contrast_table(gimps,gimps.columns)

print "Differences in variance"
print ss.coef_table(md.fit['alpha_v'],md.B.columns)
print ss.contrast_table(md.fit['alpha_v'],md.B.columns)

outliers = [1491,1489]
dout = d.query('~(sid in [1491,1489])').copy()

md = hetrobit('slope2 ~ group:time + pretest','0+group',dout,error_prior=5)
print "Model validation:"
print md.validate()
print md.validate([stat_by_group_fn('std',md,lambda x,a: np.var(x,a))])
print "WAIC: %4.0f (SE = %2.0f)" % md.WAIC()[:2]

p = pd.DataFrame(md.df.groupby(['group','time']).pretest.mean()).reset_index()
y = md.predict(p)
entries = p.shape[0]
p = p.iloc[np.repeat(np.arange(entries),y.shape[1]),:]
p['sample'] = np.tile(np.arange(y.shape[1]),entries)
p['y'] = np.reshape(y,y.shape[0]*y.shape[1])
p.set_index(['group', 'time','sample','pretest'],inplace=True)

imp = p.reset_index('pretest').query('time == 3')
imp['imp'] = imp.y/2 - imp.pretest/2
gimps = imp.imp.unstack('group')
print "Improvement from day 1 pre to day 2 post"
print ss.coef_table(gimps,gimps.columns)
print ss.contrast_table(gimps,gimps.columns)

print "Differnces in variance"
print ss.coef_table(md.fit['alpha_v'],md.B.columns)
print ss.contrast_table(md.fit['alpha_v'],md.B.columns)
