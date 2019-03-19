library(Hmisc)
## library(multcomp)
## library(car)
library(ggplot2)

data = read.csv('data.csv')

d = subset(data,group %in% c('A30','A60','A120','A240') & time == 3)

jitter = position_jitter(width=0.5)
ggplot(d,aes(x=group,y=-(slope - mean(pretest)))) +
  stat_summary(fun.data='mean_cl_boot',geom='bar',fill='gray',width=0.75) +
  stat_summary(fun.data='mean_cl_boot',geom='linerange',
               fun.args = list(conf.int=0.682)) +
  geom_text(aes(label=sid),position=jitter) +
  geom_point(position=jitter) +
  xlim('A30','A60','A120','A240') +
  theme_classic() +
  ylab("Adj. Improvement in Slope")

ggplot(d,aes(x=group,y=-(adj_slope - mean(pretest)))) +
  stat_summary(fun.data='mean_cl_boot',geom='bar',fill='gray',width=0.75) +
  stat_summary(fun.data='mean_cl_boot',geom='linerange',
               fun.args = list(conf.int=0.682)) +
  ## geom_text(aes(label=sid)) +
  geom_point(position=position_jitter(width=0.05)) +
  xlim('A30','A60','A120','A240') +
  theme_classic() +
  theme(
    axis.ticks.length=unit(-0.33,"char"),
    axis.line.x = element_line(size=0.5,linetype=1,color='black'),
    axis.line.y = element_line(size=0.5,linetype=1,color='black'),
    axis.text.y = element_text(margin=margin(0,1.2,0,0,"lines")),
    axis.text.x = element_text(margin=margin(1.2,0,0,0,"lines"))) +
  ylab("Improvement in Slope")

ggsave(paste('apamount_amount_',Sys.Date(),'.pdf',sep=''),width=3.5,height=4,
       useDingbats=F)

d = subset(data,group %in% c('A30','A60','A120','A240'))

pdodge = position_dodge(width=0.5)
ggplot(d,aes(x=time,y=adj_slope,color=group,shape=group)) +
  stat_summary(fun.data='mean_cl_boot',geom='line',position=pdodge) +
  stat_summary(fun.data='mean_cl_boot',position=pdodge,
               fun.args=list(conf.int=0.682),fill='white') +
  theme_classic() +
  scale_color_manual(values=c('darkgray','darkgray','black','black')) +
  scale_shape_manual(values=c(15,16,21,17)) +
  coord_cartesian(ylim=c(0.2,0.42)) +
  theme(
    axis.ticks.length=unit(-0.33,"char"),
    axis.line.x = element_line(size=0.5,linetype=1,color='black'),
    axis.line.y = element_line(size=0.5,linetype=1,color='black'),
    axis.text.y = element_text(margin=margin(0,1.2,0,0,"lines")),
    axis.text.x = element_text(margin=margin(1.2,0,0,0,"lines"))) +
  ylab("Pre-test Adjusted Slope") +
  xlab("") +
  scale_x_continuous(breaks=0:3,labels=c('Pre-test Day 1','Post-test Day 1',
                                         'Pre-test Day 2','Post-test Day 2'))

ggsave(paste('apamount_amount_byday_',Sys.Date(),'.pdf',sep=''),width=4,height=3,
       useDingbats=F)

# d = subset(data,group %in% c('A30','A60','A120','A240') & time == 3)
# d$group = relevel(d$group,'A30')
# m = lm(slope ~ pretest + group,d)
# summary(m)
# Anova(m)
# shapiro.test(m)

# d = subset(data,group %in% c('A30','A60','A120','A240') & time > 0)
# d$group = factor(d$group,c('A30','A60','A120','A240'))
# m = lm(slope ~ pretest + group:time,d)
# summary(m)
# Anova(m)
# shapiro.test(m)
