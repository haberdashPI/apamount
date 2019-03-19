import pandas as pd
import nu_wright_lab_util.sample_stats as ss
import numpy as np
from hetrobit import *

data = pd.read_csv('data.csv')

d = data.query("group in ['A60','npre_A60','ppre_A60']").copy()
d['slope2'] = np.minimum(d.slope*2,1.0)
m3 = hetrobit('slope2 ~ time*group','0+group',d.query('time in [0,3]'),
              error_prior=200,r=0.05)
print "Raw model coefficients:"
print m3.summary()['mean']
print m3.summary()['scale']

print "Model validation:"
print m3.validate()
print m3.validate([stat_by_group_fn('std',m3,lambda x,a: np.var(x,a))])

p = pd.DataFrame(m3.df.groupby(['group','time']).pretest.mean()).reset_index()
y = m3.predict(p)
entries = p.shape[0]
p = p.iloc[np.repeat(np.arange(entries),y.shape[1]),:]
p['sample'] = np.tile(np.arange(y.shape[1]),entries)
p['y'] = np.reshape(y,y.shape[0]*y.shape[1])
vals = p.set_index(['time','group','sample']).y.unstack(['time','group'])

print "Comparison to pre-test of A60:"
print "0 = pre-test day 1, 3 = post-test day 2"
print ss.coef_table(vals/2)
print ss.contrast_table(vals/2)

print "Comparison of variance"
print coef_table(m3.fit['alpha_v'],m3.B.columns)
print contrast_table(m3.fit['alpha_v'],m3.B.columns,round=4)

print "Comparison of means"
print contrast_table(np.dot(m3.fit['alpha'][:,0:3],
                            np.array([[1,0,0],[1,1,0],[1,0,1]]).T),
                     ['A60','npre_A60','ppre_A60'])

# outlier tests (not reported in paper)

# what if we remove the two listeners with very shallow slopes
# in
d_rem = d.query('(time == 3) & not(sid in [1554, 1557])')
m4 = hetrobit('slope2 ~ group','0+group',d_rem,
              error_prior=200,cache_file='pass_robit4.o',r=0.05)
print "mean:"
print m4.summary()['mean']
print "scale:"
print m4.summary()['scale']


print m4.validate()
print m4.validate([stat_by_group_fn('std',m4,lambda x,a: np.var(x,a))])

print coef_table(m4.fit['alpha_v'],m4.B.columns)
print contrast_table(m4.fit['alpha_v'],m4.B.columns,round=4)

print contrast_table(np.dot(m4.fit['alpha'][:,0:3],
                            np.array([[1,0,0],[1,1,0],[1,0,1]]).T),
                     ['A60','npre_A60','ppre_A60'])
