(define (problem GRID_DOMAIN_FOR_HAAI_prob01)
(:domain GRID_DOMAIN_FOR_HAAI)
(:objects
    x0 x1 x2 - xdim
    y0 y1 y2 - ydim
)
(:init
    (currentx x0)
    (currenty y0)
    (righty y0 y1)
    (righty y1 y2)
    (lefty y2 y1)
    (lefty y1 y0)
    (bottomx x2 x1)
    (bottomx x1 x0)
    (topx x0 x1)
    (topx x1 x2)
    (box x0 y2)
    (unloadbox x1 y2)
)

;;20 21 22
;;10 11 12
;;00 01 02
(:goal
(and(unfetched_box))
)
)
