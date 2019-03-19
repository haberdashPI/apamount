require(Hmisc)
require(ggplot2)

data = read.csv('data.csv')

d = subset(data,group %in% c('A60','npre_A60','ppre_A60'))

pdodge = position_dodge(width=0.5)
ggplot(d,aes(x=time,y=slope,group=group,shape=group)) +
  stat_summary(fun.data='mean_cl_boot',position=pdodge,geom='pointrange',
               fun.args=list(conf.int=0.682)) +
  stat_summary(fun.data='mean_cl_boot',position=pdodge,geom='line',
               fun.args=list(conf.int=0.682)) +
  geom_point(position=pdodge,size=1) +
  theme_classic() +
  theme(
    legend.position = "none",
    axis.ticks.length=unit(-0.33,"char"),
    axis.line.x = element_line(size=0.5,linetype=1,color='black'),
    axis.line.y = element_line(size=0.5,linetype=1,color='black'),
    axis.text.y = element_text(margin=margin(0,1.2,0,0,"lines")),
    axis.text.x = element_text(margin=margin(1.2,0,0,0,"lines"))) +
  ylab("Slope")

ggsave(paste('apamount_amount_passive_',Sys.Date(),'.pdf',sep=''),
       width=4,height=3,useDingbats=F)
# d$time = as.numeric(d$time)
# m = lm(slope ~ group + log(time+1) + pretest,d)
# summary(m)
# shapiro.test(residuals(m))

# m = lm(slope ~ group * log(time+1) + pretest,subset(d,time > 0))
# summary(m)
# shapiro.test(residuals(m))
