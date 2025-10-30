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

(** Convert a [Codicon] to a [Byo_icon]. This can be helpful if you want to use a Codicon
    with a library that accepts arbitrary icon sets. See [Byo_icon] for more details. *)
val to_byo_icon : t -> Byo_icon.t
