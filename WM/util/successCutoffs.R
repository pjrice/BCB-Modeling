
################################################################################
#t-tests


#for targets

randResp = c(0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1)
t.test(randResp, mu=0.5, alternative='greater')

nineCorrect = c(0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1)
t.test(nineCorrect, mu=0.5, alternative='greater')

tenCorrect =  c(0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1)
t.test(tenCorrect, mu=0.5, alternative='greater')

elevenCorrect =  c(0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1)
t.test(elevenCorrect, mu=0.5, alternative='greater')

#twelve correct out of 16 is significant greater than 50% random response
twelveCorrect =  c(0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1)
t.test(twelveCorrect, mu=0.5, alternative='greater')



#for lures
randResp = c(rep(0,12),rep(1,12))
t.test(randResp, mu=0.5, alternative='greater')

thirteenCorrect = c(rep(0,11),rep(1,13))
t.test(thirteenCorrect, mu=0.5, alternative='greater')

fourteenCorrect = c(rep(0,10),rep(1,14))
t.test(fourteenCorrect, mu=0.5, alternative='greater')

fifteenCorrect = c(rep(0,9),rep(1,15))
t.test(fifteenCorrect, mu=0.5, alternative='greater')

sixteenCorrect = c(rep(0,8),rep(1,16))
t.test(sixteenCorrect, mu=0.5, alternative='greater')

#seventeen correct out of 24 is significant greater than 50% random response
seventeenCorrect = c(rep(0,7),rep(1,17))
t.test(seventeenCorrect, mu=0.5, alternative='greater')


#for nonlures
randResp = c(rep(0,20),rep(1,20))
t.test(randResp, mu=0.5, alternative='greater')

twofiveCorrect = c(rep(0,15),rep(1,25))
t.test(twofiveCorrect, mu=0.5, alternative='greater')

#twenty-six correct out of 40 is significant greater than 50% random response
twosixCorrect = c(rep(0,14),rep(1,26))
t.test(twosixCorrect, mu=0.5, alternative='greater')

################################################################################
#binomial tests
#data should be a vector length two, with number of successes as first value and number of failures as second

#####################
#for targets
randResp = c(8,8)
binom.test(randResp, n=16, p=0.5, alternative='greater')

nineCorrect = c(9,7)
binom.test(nineCorrect, n=16, p=0.5, alternative='greater')

tenCorrect = c(10,6)
binom.test(tenCorrect, n=16, p=0.5, alternative='greater')

elevenCorrect = c(11,5)
binom.test(elevenCorrect, n=16, p=0.5, alternative='greater')

#twelve correct out of 16 is significant greater than 50% random response
twelveCorrect = c(12,4)
binom.test(twelveCorrect, n=16, p=0.5, alternative='greater')

#####################
#for lures
randResp = c(12,12)
binom.test(randResp, n=24, p=0.5, alternative='greater')

sixteenCorrect = c(16,8)
binom.test(sixteenCorrect, n=24, p=0.5, alternative='greater')

#seventeen correct out of 24 is significant greater than 50% random response
seventeenCorrect = c(17,7)
binom.test(seventeenCorrect, n=24, p=0.5, alternative='greater')


#####################
#for nonlures
randResp = c(20,20)
binom.test(randResp, n=40, p=0.5, alternative='greater')

twofiveCorrect = c(25,15)
binom.test(twofiveCorrect, n=40, p=0.5, alternative='greater')

#twenty-six correct out of 40 is significant greater than 50% random response
twosixCorrect = c(26,14)
binom.test(twosixCorrect, n=40, p=0.5, alternative='greater')





################################################################################################################################################################
# number of target, lure, nonlure trials for two-back is different


#####################
#for targets and lures - 16 trials in each condition
randResp = c(8,8)
binom.test(randResp, n=16, p=0.5, alternative='greater')

nineCorrect = c(9,7)
binom.test(nineCorrect, n=16, p=0.5, alternative='greater')

tenCorrect = c(10,6)
binom.test(tenCorrect, n=16, p=0.5, alternative='greater')

elevenCorrect = c(11,5)
binom.test(elevenCorrect, n=16, p=0.5, alternative='greater')

#twelve correct out of 16 is significant greater than 50% random response
twelveCorrect = c(12,4)
binom.test(twelveCorrect, n=16, p=0.5, alternative='greater')


#####################
#for nonlures - 48 trials in this condition
randResp = c(24,24)
binom.test(randResp, n=48, p=0.5, alternative='greater')

threezeroCorrect = c(30,18)
binom.test(threezeroCorrect, n=48, p=0.5, alternative='greater')

#thirty-one correct out of 48 is significant greater than 50% random response
threeoneCorrect = c(31,17)
binom.test(threeoneCorrect, n=48, p=0.5, alternative='greater')























