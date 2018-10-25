(define (domain GRID_DOMAIN_FOR_HAAI)

;; =====
;; REQUIREMENTS
;; =====

(:requirements :strips :typing)

;; =====
;; TYPES
;; =====

(:types 
	xdim ydim - coordinates

)

(:predicates

    (currentx ?ax - xdim)
    (currenty ?ay - ydim)
    (righty ?az - ydim ?ay2 - ydim)
    (lefty ?az - ydim ?ay2 - ydim) 
    (topx ?az - xdim ?ax2 - xdim) 
    (bottomx ?az - xdim ?ax2 - xdim) 
    (fetched_box)
    (boxx ?ax - xdim)
    (boxy ?ay - ydim)
    (unloadboxx ?ax - xdim)
    (unloadboxy ?ay - ydim)
    (unfetched_box)
    (observedx ?ax - xdim) 
    (observedy ?ay - ydim) 
)

(:action move_righty
    :parameters(?ax - xdim ?ay - ydim ?az - ydim)
    :precondition(and(currentx ?ax)(currenty ?ay)(righty ?ay ?az))
    :effect(and(currenty ?az)(not(currenty ?ay))(observedx ?ax)(observedy ?ay))
)

(:action move_lefty
    :parameters(?ax - xdim ?ay - ydim ?az - ydim)
    :precondition(and(currentx ?ax)(currenty ?ay)(lefty ?ay ?az))
    :effect(and(currenty ?az)(not(currenty ?ay))(observedx ?ax)(observedy ?ay))
)

(:action move_topx
    :parameters(?ax - xdim ?ay - ydim ?az - xdim)
    :precondition(and(currentx ?ax)(currenty ?ay)(topx ?ax ?az))
    :effect(and(currentx ?az)(not(currentx ?ax))(observedx ?ax)(observedy ?ay))
)

(:action move_bottomx
    :parameters(?ax - xdim ?ay - ydim ?az - xdim)
    :precondition(and(currentx ?ax)(currenty ?ay)(bottomx ?ax ?az))
    :effect(and(currentx ?az)(not(currentx ?ax))(observedx ?ax)(observedy ?ay))
)


(:action fetch_box
    :parameters(?ax - xdim ?ay - ydim)
    :precondition(and(currentx ?ax)(currenty ?ay)(boxx ?ax)(boxy ?ay)(not(fetched_box)))
    :effect(and(fetched_box)(not(unfetched_box)))
)

(:action unfetch_box
    :parameters(?ax - xdim ?ay - ydim)
    :precondition(and(currentx ?ax)(currenty ?ay)(fetched_box)(not(unfetched_box))(unloadboxx ?ax)(unloadboxy ?ay))
    :effect(and(not(fetched_box))(unfetched_box))
)
)
