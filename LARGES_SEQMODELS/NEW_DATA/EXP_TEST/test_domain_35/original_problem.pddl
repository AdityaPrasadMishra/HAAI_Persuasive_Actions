(define (problem GRID_DOMAIN_FOR_HAAI_prob01)
(:domain GRID_DOMAIN_FOR_HAAI)
(:objects
    x0 x1 x2 x3 x4 - xdim
    y0 y1 y2 y3 y4 - ydim
)
(:init
    (currentx x4)
(currenty y0)
    (righty y0 y1)
    (righty y1 y2)
    (righty y2 y3)
    (righty y3 y4)
    (lefty y4 y3)
    (lefty y3 y2)
    (lefty y2 y1)
    (lefty y1 y0)
    (bottomx x4 x3)
    (bottomx x3 x2)
    (bottomx x2 x1)
    (bottomx x1 x0)
    (topx x0 x1)
    (topx x1 x2)
    (topx x2 x3)
    (topx x3 x4)
    (boxx x1)
(boxy y0)
    (unloadboxx x4)
(unloadboxy y3)
)

;;20 21 22
;;10 11 12
;;00 01 02
(:goal
(and
    (unfetched_box)
    (observedx x0)
(observedy y0)
)
)
)
