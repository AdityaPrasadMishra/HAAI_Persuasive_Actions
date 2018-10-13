(define (domain GRID_DOMAIN_FOR_HAAI)

;; =====
;; REQUIREMENTS
;; =====

(:requirements :strips :typing)

;; =====
;; TYPES
;; =====

(:types 
	
    steps direction location  - objects

)

(:predicates

    (current ?cl - location)
    (right ?cl - location ?cl1 - location)
    (left ?cl - location ?cl1 - location) 
    (top ?cl - location ?cl1 - location) 
    (bottom ?cl - location ?cl1 - location) 
    (fetched_box)
    (box ?cl - location)
    (unloadbox ?cl - location)
    (unfetched_box)
    (observed ?cl - location) 
)

(:action Move_Right
    :parameters(?cl - location ?cl1 - location)
    :precondition(and(current ?cl)(right ?cl ?cl1))
    :effect(and(current ?cl1)(not(current ?cl))(observed ?cl))
)

(:action Move_Left
    :parameters(?cl - location ?cl1 - location)
    :precondition(and(current ?cl)(left ?cl ?cl1))
    :effect(and(current ?cl1)(not(current ?cl))(observed ?cl))
)

(:action Move_top
    :parameters(?cl - location ?cl1 - location)
    :precondition(and(current ?cl)(top ?cl ?cl1))
    :effect(and(current ?cl1)(not(current ?cl))(observed ?cl))
)

(:action Move_bottom
    :parameters(?cl - location ?cl1 - location)
    :precondition(and(current ?cl)(bottom ?cl ?cl1))
    :effect(and(current ?cl1)(not(current ?cl))(observed ?cl))
)

(:action fetch_box
    :parameters(?cl - location)
    :precondition(and(current ?cl)(box ?cl)(not(fetched_box)))
    :effect(and(fetched_box)(not(unfetched_box)))
)

(:action unfetch_box
    :parameters(?cl - location)
    :precondition(and(current ?cl)(fetched_box)(not(unfetched_box))(unloadbox ?cl))
    :effect(and(not(fetched_box))(unfetched_box))
)

; (:action observe
;     :parameters(?cl - location)
;     :precondition(and(current ?cl)(fetched_box)(observe ?cl))
;     :effect(and(observed ?cl))
; )
)