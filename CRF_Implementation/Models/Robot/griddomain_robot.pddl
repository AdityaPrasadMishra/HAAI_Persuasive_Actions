(define (domain GRID_DOMAIN_FOR_HAAI)

;; =====
;; REQUIREMENTS
;; =====

(:requirements :strips :typing)

;; =====
;; TYPES
;; =====

(:types 
	xdim,ydim - coordinates

)

(:predicates

    (current ?x - xdim ?y - ydim)
    (righty ?y1 - ydim ?y2 - ydim)
    (lefty ?y1 - ydim ?y2 - ydim) 
    (topx ?x1 - xdim ?x2 - xdim) 
    (bottomx ?x1 - xdim ?x2 - xdim) 
    (fetched_box)
    (box ?x - xdim ?y - ydim)
    (unloadbox ?x - xdim ?y - ydim)
    (unfetched_box)
    (observed ?x - xdim ?y - ydim) 
)

(:action Move_Righty
    :parameters(?x - xdim ?y - ydim ?y1 - ydim)
    :precondition(and(current ?x ?y)(righty ?y ?y1))
    :effect(and(current ?x ?y1)(not(current ?x ?y))(observed ?x ?y))
)

(:action Move_Lefty
    :parameters(?x - xdim ?y - ydim ?y1 - ydim)
    :precondition(and(current ?x ?y)(lefty ?y ?y1))
    :effect(and(current ?x ?y1)(not(current ?x ?y))(observed ?x ?y))
)

(:action Move_Topx
    :parameters(?x - xdim ?y - ydim ?x1 - xdim)
    :precondition(and(current ?x ?y)(topx ?x ?x1))
    :effect(and(current ?x1 ?y)(not(current ?x ?y))(observed ?x ?y))
)

(:action Move_Bottomx
    :parameters(?x - xdim ?y - ydim ?x1 - xdim)
    :precondition(and(current ?x ?y)(bottomx ?x ?x1))
    :effect(and(current ?x1 ?y)(not(current ?x ?y))(observed ?x ?y))
)


(:action fetch_box
    :parameters(?x - xdim ?y - ydim)
    :precondition(and(current ?x ?y )(box ?x ?y)(not(fetched_box)))
    :effect(and(fetched_box)(not(unfetched_box)))
)

(:action unfetch_box
    :parameters(?x - xdim ?y - ydim)
    :precondition(and(current ?x ?y)(fetched_box)(not(unfetched_box))(unloadbox ?x ?y))
    :effect(and(not(fetched_box))(unfetched_box))
)
)