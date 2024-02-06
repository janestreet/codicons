open! Core
open! Virtual_dom
include module type of Svg

val svg
  :  ?size:[< Css_gen.Length.t ]
  -> ?color:[< Css_gen.Color.t ]
  -> ?extra_attrs:Vdom.Attr.t list
  -> t
  -> Vdom.Node.t

val name : t -> string
val all : t list
