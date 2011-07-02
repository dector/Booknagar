# Number of lists in booklete
listsInBooklete = 5

PAGES_ON_LIST = 4
PAGES_IN_BOOKLETE = listsInBooklete * PAGES_ON_LIST

chapNumber = 19
pagesNumber = 14

currentBookleteNumber = 1

while (currentBookleteNumber-1) * PAGES_IN_BOOKLETE < pagesNumber :
    execStr = "psselect -p "

    maxPage = PAGES_IN_BOOKLETE * currentBookleteNumber
    if maxPage > pagesNumber :
        maxPage = pagesNumber

    minPage = (currentBookleteNumber-1) * PAGES_IN_BOOKLETE + 1

    chapStr = str(chapNumber) + "_" + str(currentBookleteNumber)

    execStr += str(minPage) + "-" + str(maxPage) + " chap" + str(chapNumber) + ".ps "
    execStr += "chap" + chapStr + ".ps; psbook chap" + chapStr + ".ps | psnup -2 -l -p a4 > print"
    execStr += chapStr + ".ps; rm chap" + chapStr + ".ps"
    print execStr

    currentBookleteNumber += 1

print "mkdir " + str(chapNumber) + "; rm -f chap" + str(chapNumber) + "*" + "; mv print" + str(chapNumber) + "_* " + str(chapNumber)
