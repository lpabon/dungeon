import os
import sys


myclock = 725
towel_ready = True
mask_on = False
leia_in_crate = False


print "Sit up"
print "Checking clock"
if myclock < 715:
	print "Going back to sleep"
	sys.exit(0)
elif myclock > 800:
	print "Oh crap!"

if mask_on:
	print "Turn of mask"
else:
	print "What the heck, My mask is not on!!"

if leia_in_crate:
	print "Taking leia out of crate"

print "Taking leia outside"
print "Go to bathroom to take a shower"
print "Checking for a towel"
if not towel_ready:
	print "Go to the closet and get a fresh one"
print "Take a shower"


