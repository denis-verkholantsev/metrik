update Skill
filter .id = <uuid>$source
and .tree.id = <uuid>$tree
set {
    contains += (
        select detached Skill
        filter .id = <uuid>$target
        and .tree.id = <uuid>$tree
    )
};
