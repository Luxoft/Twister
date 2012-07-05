set resid1 [createEmptyResource 0]
set resid2 [createEmptyResource 0]

setProperty $resid1 "prop_1" "value_1"
puts [getProperty $resid1 "prop_1" ]

setProperty $resid2 "prop_2" "value_2"
puts [getProperty $resid2 "prop_2"]

setProperty $resid2 "prop_11" "value_11"
puts [getProperty $resid2 "prop_11" ]

delResource $resid1
delResource $resid2

return "PASS"
