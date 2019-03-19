from nu_wright_lab_util import regress as r
from nu_wright_lab_util import blmm
import patsy
import os
import numpy as np
import scipy
from nu_wright_lab_util.sample_stats import *

hetrobit_model = blmm.load_model('hetrobit')


def stat_by_group_fn(name,model,stat_fn):
  df = model.df

  def fn(diffs,axis):
    results = []
    for gname,group in df.groupby('group'):
      indices = np.where(df.group == gname)[0]
      if axis == 1:
        results.append(pd.DataFrame({'value': stat_fn(diffs[:,indices],axis),
                       'type': str(gname)+name}))
      elif axis == 0:
        results.append(pd.DataFrame({'value': stat_fn(diffs[indices,:],axis),
                       'type': str(gname)+name}))
      else: assert False

    return pd.concat(results)
  return fn


def hetrobit(formula,varformula,df,coef_prior=5,error_prior=100,cache_file=None,
             r=1e-10,**sample_kws):

  y,A = patsy.dmatrices(formula,df,return_type='dataframe',eval_env=1)
  B = patsy.dmatrix(varformula,df,return_type='dataframe',eval_env=1)
  y = np.squeeze(y)

  if cache_file is None or not os.path.isfile(cache_file):
    fit = hetrobit_model.sampling({'y': y, 'A': A, 'n': A.shape[0],
                                   'k': A.shape[1],
                                   'B': B, 'h': B.shape[1],
                                   'fixed_mean_prior': coef_prior,
                                   'prediction_error_prior': error_prior,
                                   'r': r},
                                  **sample_kws)
    if cache_file:
      blmm.write_samples(fit.extract(),cache_file)
  else:
    fit = blmm.read_samples(cache_file)

  return HetRobit(r,B,fit,y,A,df)


class HetRobit(r.BaseRegressResults):
  def __init__(self,r,B,*params):
    self.r = r
    self.B = B
    super(HetRobit,self).__init__(*params)

  def summary(self,coefs=None,v_coefs=None):
      v_columns = self.B.columns
      if v_coefs is not None:
        v_columns = v_columns[v_coefs]
      v_table = coef_table(self.fit['alpha_v'],v_columns)

      c_table = super(HetRobit,self).summary(coefs)
      return {'mean': c_table,'scale': v_table}

  def _predict_helper(self,A):
    p = np.einsum('ij,kj->ik',A,self.fit['alpha'])
    r = self.r
    p = 1 / (1 + np.exp(-p))
    p = (p - r/2) / (1-r)

    return p

  def log_posterior(self,y,B=None):
    if not B:
      B = self.B
    scale = np.einsum('ij,kj->ik',B,self.fit['alpha_v'])
    r = self.r

    y = y[:,np.newaxis]
    p = r/2 + self.predict()*(1-r)

    return scipy.stats.beta.logpdf(r/2 + y*(1-r),p*scale,(1-p)*scale)

  def error_fn(self):
    r = self.r
    alpha_v = self.fit['alpha_v']
    B = self.B

    def fn(y_hat,indices,r=r):
      y_hat = y_hat[indices,:]

      p = r/2 + y_hat*(1-r)
      scale = np.einsum('ij,kj->ki',B,alpha_v[indices,:])
      pr = np.random.beta(p*scale,(1-p)*scale)
      pr = (pr - r/2) / (1-r)

      return pr - y_hat

    return fn
