# Setup -------------------------------------------------------------------
library(ggplot2)
library(dplyr)
library(scales)
library(reshape2)
rm(list = ls())

# Location of data and also where the plots will be saved
DIR_LOC <- '/Users/josiahdavis/Documents/Berkeley/STAT222/data/'

# Read data and formatting ------------------------------------------------

d <- read.csv(paste0(DIR_LOC, 'results.csv'))

d$strategy <- factor(d$strategy, levels = c(0, 1, 2)
                     , labels = c('Equal Weight', 'Minimize Risk', 'Maximize Returns'))

d$period_train <- factor(d$period
                         , levels = c(1, 2, 3, 4, 5)
                         , labels = c('1986-1990', '1991-1995', '1996-2000', '2001-2005', '2006-2010'))

# Plot the results from the TRAIN periods ------------------------------
avgs_train <- d %>% filter(test == 0) %>% group_by(period_train, strategy) %>% 
  summarize(risk = mean(risk), return = mean(return))

train <- ggplot(d[d$test == 0,], aes(y = return, x = risk, color = strategy)) + 
  geom_point(size = 3.5, alpha = .65) + 
  facet_wrap(~ period_train) + 
  geom_hline(data = avgs_train, aes(yintercept = return, color = strategy)) + 
  geom_vline(data = avgs_train, aes(xintercept = risk, color = strategy)) + 
  theme(legend.title = element_blank()
        , legend.justification=c(1,0), legend.position=c(.95,.15)) + 
  labs(title = ''
       , subtitle = ''
       , x = 'Risk'
       , y = 'Return'
       , caption = 'Source: Yahoo! Finance')
plot(train)
ggsave(train, device = 'png', width = 8, height = 6, filename = paste0(DIR_LOC, 'train.png'))

# Plot the results from the TEST periods ------------------------------
d$period_test <- factor(d$period
                          , levels = c(1, 2, 3, 4, 5)
                          , labels = c('1992-1996', '1997-2001', '2002-2006', '2007-2011', '2012-2016'))

avgs_test <- d %>% filter(test == 1) %>% group_by(period_test, strategy) %>% 
  summarize(risk = mean(risk), return = mean(return))

test <- ggplot(d[d$test == 1,], aes(y = return, x = risk, color = strategy)) + 
  geom_point(size = 3.5, alpha = .65) + 
  facet_wrap(~ period_test) + 
  geom_hline(data = avgs_test, aes(yintercept = return, color = strategy)) + 
  geom_vline(data = avgs_test, aes(xintercept = risk, color = strategy)) + 
  theme(legend.title = element_blank()
        , legend.justification=c(1,0), legend.position=c(.95,.15)) + 
  labs(title = ''
       , subtitle = ''
       , x = 'Risk'
       , y = 'Return'
       , caption = 'Source: Yahoo! Finance')
ggsave(test, device = 'png', width = 8, height = 6, filename = paste0(DIR_LOC, 'test.png'))
print(test)


# Plot the bonds returns --------------------------------------------------

d2 <- read.csv(paste0(DIR_LOC, 'Bonds86.csv'))
d2 <- melt(d2, id.vars = 'Date')
d2$Date2 <- as.POSIXct(d2$Date)
old_names <- c('Date', 'Naive', 'Naive.w.o.NVR', 'Basic', 'Adjusted', 'Basic.Bond', 
               'Bond.Ladder', 'Increasing.Bond', 'Increasing.Ladder')
new_names <- c('Date', 'Naive_all', 'Naive', 'Basic', 'Adjusted', 'Basic Bond', 
               'Bond Ladder', 'Increasing Bond', 'Increasing Ladder')
d2$variable <- factor(d2$variable, levels = old_names, labels = new_names)
# d2$shape <- 1
# d2$shape <- ifelse(d2$variable %in% c('Naive'), 16, d2$shape) # filled circle
# d2$shape <- ifelse(d2$variable %in% c('Single Opt', 'Basic Bonds', 'Increasing Ladder'), 15, d2$shape) # filled square
# d2$shape <- ifelse(d2$variable %in% c('Multiperiod', 'Bond Ladder', 'Inceasing Bond'), 17, d2$shape) # filled triangle
# d2$shape <- factor(d2$shape)

ggplot(d2[d2$variable != 'Naive_all',], aes(x = Date2, y = value, group = variable, color = variable)) + 
  geom_line() + 
  geom_point(aes(shape = variable), size = 3) + 
  scale_x_datetime(breaks = date_breaks('5 years'), labels = date_format('%Y')) + 
  labs(x = '', y = 'Relative Return') + 
  theme(legend.title = element_blank())
