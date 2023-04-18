

list_to_parse=['Sun\nApr 9\n0h 00m', 'Sun\nApr 9', '', 'Sun', 'Apr 9', '0h 00m', '0h 00m', '0h 00m', '', '', 'Mon\nApr 10\n0h 00m\nEaster Monday', 'Mon\nApr 10', '', 'Mon', 'Apr 10', '0h 00m\nEaster Monday', '0h 00m\nEaster Monday', '0h 00m\nEaster Monday', '', 'Easter Monday', '', 'Tue\nApr 11\n0h 00m', 'Tue\nApr 11', '', 'Tue', 'Apr 11', '0h 00m', '0h 00m', '0h 00m', '', 'Wed\nApr 12\n0h 00m', 'Wed\nApr 12', '', 'Wed', 'Apr 12', '0h 00m', '0h 00m', '0h 00m', '', 'Thu\nApr 13\n7h 30m', 'Thu\nApr 13', '', 'Thu', 'Apr 13', '7h 30m', '7h 30m', '7h 30m', '', '', '', '', '', 'Fri\nApr 14\n7h 30m', 'Fri\nApr 14', '', 'Fri', 'Apr 14', '7h 30m', '7h 30m', '7h 30m', '', '', '', '', '', 'Sat\nApr 15\n0h 00m', 'Sat\nApr 15', '', 'Sat', 'Apr 15', '0h 00m', '0h 00m', '0h 00m', '', 'Sun\nApr 16\n0h 00m', 'Sun\nApr 16', '', 'Sun', 'Apr 16', '0h 00m', '0h 00m', '0h 00m', '', '', 'Mon\nApr 17\n7h 30m\n7h 30m\nLiberty Global Automation & AI', 'Mon\nApr 17', '', 'Mon', 'Apr 17', '7h 30m\n7h 30m\nLiberty Global Automation & AI', '7h 30m\n7h 30m\nLiberty Global Automation & AI', '7h 30m\n7h 30m\nLiberty Global Automation & AI', '7h 30m\nLiberty Global Automation & AI', '', '7h 30m\nLiberty Global Automation & AI', 'Liberty Global Automation & AI', '', 'Tue\nApr 18\n7h 30m', 'Tue\nApr 18', '', 'Tue', 'Apr 18', '7h 30m', '7h 30m', '7h 30m', '', '', '', '', '', 'Wed\nApr 19\n7h 30m', 'Wed\nApr 19', '', 'Wed', 'Apr 19', '7h 30m', '7h 30m', '7h 30m', '', '', '', '', '', 'Thu\nApr 20\n7h 30m', 'Thu\nApr 20', '', 'Thu', 'Apr 20', '7h 30m', '7h 30m', '7h 30m', '', '', '', '', '', 'Fri\nApr 21\n7h 30m', 'Fri\nApr 21', '', 'Fri', 'Apr 21', '7h 30m', '7h 30m', '7h 30m', '', '', '', '', '', 'Sat\nApr 22\n0h 00m', 'Sat\nApr 22', '', 'Sat', 'Apr 22', '0h 00m', '0h 00m', '0h 00m', '']
list_to_parse.remove('Liberty Global Automation & AI')
nonempty_list = list(filter(None, list_to_parse))# remove empty strings

#remove the hours

nonempty_list=list((filter(lambda value:'7h 30m' not in value,  nonempty_list)))
nonempty_list=list((filter(lambda value:'0h 00m' not in value,  nonempty_list)))
nonempty_list=list((filter(lambda value:'\n' not in value,  nonempty_list)))

print(nonempty_list)
#nonempty_list= [value for value in nonempty_list if '7h 30m' not in value] 
#nonempty_list= [value for value in nonempty_list if '0h 00m' not in value]





