begin_version
3
end_version
begin_metric
0
end_metric
6
begin_variable
var0
-1
3
Atom currentx(x0)
Atom currentx(x1)
Atom currentx(x2)
end_variable
begin_variable
var1
-1
3
Atom currenty(y0)
Atom currenty(y1)
Atom currenty(y2)
end_variable
begin_variable
var2
-1
2
Atom fetched_box()
NegatedAtom fetched_box()
end_variable
begin_variable
var3
-1
2
Atom unfetched_box()
NegatedAtom unfetched_box()
end_variable
begin_variable
var4
-1
2
Atom observedy(y2)
NegatedAtom observedy(y2)
end_variable
begin_variable
var5
-1
2
Atom observedx(x2)
NegatedAtom observedx(x2)
end_variable
0
begin_state
2
2
1
1
1
1
end_state
begin_goal
3
3 0
4 0
5 0
end_goal
31
begin_operator
fetch_box x2 y2
2
0 2
1 2
2
0 2 1 0
0 3 -1 1
1
end_operator
begin_operator
move_bottomx x1 y0 x0
1
1 0
1
0 0 1 0
1
end_operator
begin_operator
move_bottomx x1 y1 x0
1
1 1
1
0 0 1 0
1
end_operator
begin_operator
move_bottomx x1 y2 x0
1
1 2
1
0 0 1 0
1
end_operator
begin_operator
move_bottomx x2 y0 x1
1
1 0
1
0 0 2 1
1
end_operator
begin_operator
move_bottomx x2 y1 x1
1
1 1
1
0 0 2 1
1
end_operator
begin_operator
move_bottomx x2 y2 x1
1
1 2
1
0 0 2 1
1
end_operator
begin_operator
move_lefty x0 y1 y0
1
0 0
1
0 1 1 0
1
end_operator
begin_operator
move_lefty x0 y2 y1
1
0 0
1
0 1 2 1
1
end_operator
begin_operator
move_lefty x1 y1 y0
1
0 1
1
0 1 1 0
1
end_operator
begin_operator
move_lefty x1 y2 y1
1
0 1
1
0 1 2 1
1
end_operator
begin_operator
move_lefty x2 y1 y0
1
0 2
1
0 1 1 0
1
end_operator
begin_operator
move_lefty x2 y2 y1
1
0 2
1
0 1 2 1
1
end_operator
begin_operator
move_righty x0 y0 y1
1
0 0
1
0 1 0 1
1
end_operator
begin_operator
move_righty x0 y1 y2
1
0 0
1
0 1 1 2
1
end_operator
begin_operator
move_righty x1 y0 y1
1
0 1
1
0 1 0 1
1
end_operator
begin_operator
move_righty x1 y1 y2
1
0 1
1
0 1 1 2
1
end_operator
begin_operator
move_righty x2 y0 y1
1
0 2
1
0 1 0 1
1
end_operator
begin_operator
move_righty x2 y1 y2
1
0 2
1
0 1 1 2
1
end_operator
begin_operator
move_topx x0 y0 x1
1
1 0
1
0 0 0 1
1
end_operator
begin_operator
move_topx x0 y1 x1
1
1 1
1
0 0 0 1
1
end_operator
begin_operator
move_topx x0 y2 x1
1
1 2
1
0 0 0 1
1
end_operator
begin_operator
move_topx x1 y0 x2
1
1 0
1
0 0 1 2
1
end_operator
begin_operator
move_topx x1 y1 x2
1
1 1
1
0 0 1 2
1
end_operator
begin_operator
move_topx x1 y2 x2
1
1 2
1
0 0 1 2
1
end_operator
begin_operator
unfetch_box x2 y2
2
0 2
1 2
2
0 2 0 1
0 3 1 0
1
end_operator
begin_operator
waiting x0 y2
1
3 0
1
0 4 -1 0
1
end_operator
begin_operator
waiting x1 y2
1
3 0
1
0 4 -1 0
1
end_operator
begin_operator
waiting x2 y0
1
3 0
1
0 5 -1 0
1
end_operator
begin_operator
waiting x2 y1
1
3 0
1
0 5 -1 0
1
end_operator
begin_operator
waiting x2 y2
1
3 0
2
0 5 -1 0
0 4 -1 0
1
end_operator
0
