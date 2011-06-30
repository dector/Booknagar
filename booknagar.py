# Number of lists in booklete
listsInBooklete = 5

PAGES_ON_LIST = 4
PAGES_IN_BOOKLETE = listsInBooklete * PAGES_ON_LIST

pagesNumber = 80
currentBookleteNumber = 1

while (currentBookleteNumber-1) * PAGES_IN_BOOKLETE < pagesNumber :
    currentPage = (currentBookleteNumber-1) * PAGES_IN_BOOKLETE + 1
    evenPagesList = []
    oddPagesList = []

    while currentPage <= PAGES_IN_BOOKLETE * currentBookleteNumber :
        if currentPage <= pagesNumber :
            if currentPage % 2 == 1 :
                evenPagesList.append(currentPage)
            else :
                oddPagesList.append(currentPage)
        currentPage += 1

    print "=== Booklete #" + str(currentBookleteNumber) + " ===";

    s = "All pages: " + str((currentBookleteNumber-1) * PAGES_IN_BOOKLETE + 1) + "-"
    s += str(PAGES_IN_BOOKLETE * currentBookleteNumber)
    print s
    #for evenPage in evenPagesList :
    #    s += str(evenPage) + ","
    #for oddPage in oddPagesList :
    #    s += str(oddPage) + ","
    #print s[:-1]

    s = "Even pages: "
    for evenPage in evenPagesList :
        s += str(evenPage) + ","
    print s[:-1]

    s = "Odd pages: "
    for oddPage in oddPagesList :
        s += str(oddPage) + ","
    print s[:-1]
 
    currentBookleteNumber += 1
