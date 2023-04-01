// ----------------------
// expected output
// 1
// done
// ----------------------
if true {
	print 1
}

print "\n"

if false {
	print 99  // shouldn't execute
}

print "done"
